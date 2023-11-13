from rest_framework import serializers
from django.contrib.auth.models import User
from solarit.models import Solarit_Docs, Template






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



    

class SolaritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solarit_Docs
        fields = '__all__'



class Template_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'






        


