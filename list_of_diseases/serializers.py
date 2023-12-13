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



class DrugSerializer(serializers.ModelSerializer):

    disease = DiseaseSerializer(read_only = True, many=True, source='for_disease')
    
    class Meta:
        model = Medical_drug
        fields= "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'is_staff', 'is_superuser')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)
        is_superuser = validated_data.pop('is_superuser', False)

        user = CustomUser.objects.create(
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])

        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save()

        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_moderator')
