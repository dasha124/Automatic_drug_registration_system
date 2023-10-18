# поля, которые вы хотели бы, чтобы преобразовывались в JSON и отправлялись клиенту.
# Сериализаторы были придуманы для того, чтобы преобразовывать наши модели из базы данных в JSON и наоборот.
from .models import *
from rest_framework import serializers


# заболевание = услуга
class DiseaseSerializer(serializers.ModelSerializer):
   
    class Meta:
        # Модель, которую мы сериализуем
        model = Disease
        # Поля, которые мы сериализуем
        fields= "__all__"


class DiseaseNameSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Disease
        # Поля, которые мы сериализуем
        fields= ['disease_name']


class DrugSerializer(serializers.ModelSerializer):

    disease = DiseaseSerializer(read_only = True, many=True, source='for_disease')
    
    class Meta:
        model = Medical_drug
        fields= "__all__"
