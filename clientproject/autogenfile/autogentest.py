import os
import autogen
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')

config_list = [
    {
    'model': 'gpt-4',
    'api_key': api_key
    },
    {
    'model': 'gpt-3.5-turbo-1106',
    'api_key': api_key
    },
]



config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-3"]
    }
)


# Assistant Agent

assistant = autogen