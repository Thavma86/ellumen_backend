from django.shortcuts import render
import json
import pickle
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .models import Solarit_Docs
from .models import Template
import requests
# Document libraries
# import docx
from api.serializer import SolaritSerializer, Template_Serializer
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from rest_framework.decorators import api_view
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter



load_dotenv()
llm = ChatOpenAI( model_name="gpt-3.5-turbo", temperature=0.2, max_tokens=30)




# API to get Chatbot System Role   
def get_chatbot_system_role():
    system_template = Template.objects.first()
    if system_template:
         serializer = Template_Serializer(system_template, many=False)
         return Response({"message": serializer.data})
    else:
        return Response({"message": "No system template"})       

# Prompt 
def handle_prompts(user_input):
    try:
        retrieved_system_role = get_chatbot_system_role()
        template = f"""
                You are a Customer Service Rep for a Solar company called Solarit.
                        Check here for more information:{retrieved_system_role}
                        The role play scenerio would look like this:
                         
                        """
        prompt = ChatPromptTemplate(
        messages=[
        SystemMessagePromptTemplate.from_template(template=template),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
        ]
        )
        return prompt
    except:
        return ValueError("Problem with handle_prompts")
    



# Extract text from Txt Documents
def extract_raw_text_from_txt_documents():
    try:
        txt_file_path = os.path.join(settings.MEDIA_ROOT, "txt_documents")
        all_files = [file for file in os.listdir(txt_file_path) if file.endswith('.txt')]
        raw_text_for_txt_doc = ""
        for file in all_files:
            join_files_with_path = os.path.join(txt_file_path, file)
        with open(join_files_with_path, 'r') as f:
            file_content = f.read()
            raw_text_for_txt_doc += file_content
        return raw_text_for_txt_doc
    except:
        return ValueError("Problem with extract_raw_text_from_txt_documents function ")
        

# Collate texts from all documents
def get_text_from_all_documents_into_single_array():
    try:
        all_texts = []
        raw_text_for_txt_doc = extract_raw_text_from_txt_documents()
        all_texts.append(raw_text_for_txt_doc)
        single_text = '\ln'.join(all_texts)
        return single_text
    except:
        return ValueError("get_text_from_all_documents_into_single_array")
        
# Split raw text into chunks
def split_raw_text_into_chunks(all_raw_texts):
    try:
        chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
            )
        chunks = chunk_splitter.create_documents([all_raw_texts])
        print(f"Length of chunks splitted is: {len(chunks)}")
        print(chunks)
        return chunks
    except:
        return ValueError("Problem with split_raw_text_into_chunks function")


# Retrieve data from database model
def retrieve_data_from_database_model():
    try:
        template_data = Template.objects.first()
        if template_data:
            retrieved_template = template_data.template
               
        else:
            raise ValueError("Not able to find system prompt")
        return retrieved_template
    except:
        return ValueError("Problem with retrieve_data_from_database_model function")

        
# Count tokens used
def count_tokens(conversation, user_input):
    try:
        with get_openai_callback() as cb:
            result = conversation.run(question=user_input)
            print(f"Spent a total of {cb.total_tokens} tokens")
        return result
    except:
        return ValueError("Problem with count_tokens function")

 
        
def run_conversation(prompt, memory):
    try:
        conversation = LLMChain(
                llm=llm,
                prompt=prompt,
                verbose=False,
                memory=memory
                )
        return conversation
    except:
        return "Problem with run_conversation function"
        
       
      


# API for Get view to display all documents e.g .docx,txt,pdf
@api_view(['GET'])
def get_all_serialized_documents(request):
    try:
        files = Solarit_Docs.objects.all()
        serializer = SolaritSerializer(files, many=True)
        return Response({'data': serializer.data})
    except:
        return ValueError("Problem with get_serialized_files function")


# API to save documents
@csrf_exempt
@api_view(['POST'])
def save_docs(request):
    if request.method == 'POST' and 'document' in request.FILES:
        uploaded_file = request.FILES['document']
        document_title = request.data.get("title")
        filename = uploaded_file.name.lower()
        file_extension = uploaded_file.name.split('.')[-1].lower()

        allowed_extensions = ['txt', 'pdf', 'csv', 'json']
        if file_extension in allowed_extensions and file_extension == "txt":
            # File saving
            solarit_docs = Solarit_Docs(txt_documents=uploaded_file, title=document_title) 
            solarit_docs.save()
            data = uploaded_file.read()
            print(data)
            return Response({'filemessage': f'Your file named "{filename}"  was uploaded. Please referesh'})
            
        else:
            return Response({'filemessage':'Only ".txt" files are currently being processed. Other files are being added in batches. Check back soon.'})
    
    else:
        return Response({'message': 'Your request was not processed'})
    


# API to Delete Documents
@api_view(['POST'])
def delete_doc(request, documentid):
    if request.method == 'POST':
        document = Solarit_Docs.objects.filter(id=documentid).first()
        if document:
            document.delete()
            print(f"{document} was deleted")
            return Response({'filemessage': f'Document {documentid} has been deleted', "status": status.HTTP_200_OK })
        else:
            print(f"{document} was not found")
            return Response({'filemessage': f'Document {documentid} was not found'})



# API to post Chatbot System Role        
@api_view(['POST'])
def post_chatbot_system_role(request):
     if request.method == 'POST':
         new_template_data = request.data.get('template')
     if new_template_data:
         system_template = Template.objects.first()
         if system_template:
             system_template.template = new_template_data
             system_template.save()
         print("Template added")
         return Response({"message": "Template has been updated. Please referesh."})
     else:
         return Response({"message": "Problem updating template"})






# Get Chatbot Response
@api_view(['POST'])
@csrf_exempt
def get_chatbot_response(request):
    
    try:
        
        if request.method == 'POST':
            user_input = request.data.get('payload')
           
            # Use data for user queries
            if user_input:
                prompt = handle_prompts(user_input)
                memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=4)
                conversation = run_conversation(prompt, memory)
                response = conversation.run(question = user_input)
                count_tokens(conversation, user_input)
                data = []
                data.append(response)
                print(response)
                return Response({"message": data})
            else:
                return "Error with user_input variable"
        else: 
            return Response({"message": "Error with request from user"})
        
    except Exception as e:
        return Response({"message": str(e)})

    















