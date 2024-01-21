from django.utils import timezone
from django.db.models import Q
# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import date
from django.db import connection
from django.http import JsonResponse

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from list_of_diseases.serializers import *
from list_of_diseases.models import *
from rest_framework.decorators import api_view
from operator import itemgetter
# from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import redis
import uuid
from .permissions import *
import json
from django.contrib.sessions.models import Session
from .jwt_tokens import *
from django.core.cache import cache
from base64 import b64encode
from django.core.files.base import ContentFile
import requests
from drf_yasg.utils import swagger_auto_schema

def get_session_id(request):
    session = request.COOKIES.get('session_id')
    if session is None:
        session = request.data.get('session_id')
    if session is None:
        authorization_header = request.headers.get("Authorization")
        if authorization_header and authorization_header.lower().startswith("bearer "):
            session = authorization_header[len("bearer "):]
        else:
            session = authorization_header
    return session




@swagger_auto_schema(method='post',request_body=UserRegisterSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    # Ensure username and passwords are posted is properly
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Create user
    user = serializer.save()
    message = {
        'message': 'Пользователь успешно зарегистрирован',
        'user_id': user.id
    }

    return Response(message, status=status.HTTP_201_CREATED)
    

@swagger_auto_schema(method='post',request_body=UserLoginSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def login_view(request):
    # Проверка входных данных
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        print(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Аутентификация пользователя
    user = authenticate(request, **serializer.validated_data)
    if user is None:
        message = {"message": "Пользователь не найден"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    # Создание токена доступа
    access_token = create_access_token(user.id)

    # Сохранение данных пользователя в кеше
    user_data = {
        "user_id": user.id,
        "user_name": user.username,
        "user_email": user.email,
        "is_superuser": user.is_superuser,
        "access_token": access_token
    }
    access_token_lifetime = settings.ACCESS_TOKEN_LIFETIME
    cache.set(access_token, user_data, access_token_lifetime)

    # Отправка ответа с данными пользователя и установкой куки
    response_data = {
        "user_id": user.id,
        "user_name": user.username,
        "user_email": user.email,
        "is_superuser": user.is_superuser,
        "access_token": access_token
    }
    response = Response(response_data, status=status.HTTP_201_CREATED)
    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime, samesite=None, secure=True)

    return response
    
@swagger_auto_schema(method='POST')
@api_view(["POST"])
@permission_classes([AllowAny])
def check(request):
    access_token = get_access_token(request)
    print("check = ", access_token)

    if access_token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)
    if not cache.has_key(access_token):
        message = {"message": "Token is not valid"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    user_data = cache.get(access_token)
    return Response(user_data, status=status.HTTP_200_OK)





@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
   
    access_token = get_access_token(request)
    print("logout = ", access_token)

    if access_token is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if cache.has_key(access_token):
        cache.delete(access_token)

    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie('access_token')

    return response





# список заболеваний (услуг)
@api_view(['GET'])
@permission_classes([AllowAny])
@swagger_auto_schema(method='GET')
def get_diseases(request, format=None):
    disease_name_r = request.GET.get('disease_name')
    drugID=0
    token = get_access_token(request)
    if token != 'undefined':
        payload = get_jwt_payload(token)
        user_id = payload["user_id"]
        curr_user = CustomUser.objects.get(id = user_id)
        print("uuuuuuu", curr_user)

        # try {        #     drug = Medical_drug.objects.get(user_id_id=user_id, status=0)
        if curr_user.is_superuser:
            print("ffbakjfkajf")
            if disease_name_r:
                diseases = Disease.objects.filter(
                    Q(disease_name__icontains=disease_name_r.lower())
                )       
            else:
                diseases = Disease.objects.all()
                print(diseases)
            try:
                drug = Medical_drug.objects.get(user_id_id=user_id, status=0)
                drugID = drug.id
            except Medical_drug.DoesNotExist:
                drugID = 0
        else:
            try:
                drug = Medical_drug.objects.get(user_id_id=user_id, status=0)
                drugID = drug.id
            except Medical_drug.DoesNotExist:
                drugID = 0

            if disease_name_r:
                diseases = Disease.objects.filter(
                    Q(status='a') &
                    Q(disease_name__icontains=disease_name_r.lower())
                )
            else:
                diseases = Disease.objects.filter(
                    Q(status='a')
                )

        serialized_diseases = []
        for disease in diseases:
            serializer = DiseaseSerializer(disease)
            serialized_diseases.append(serializer.data)
        serialized_diseases.append({"drugID": drugID})

        return Response(serialized_diseases)

    else:
        drugID=0
        print('here')
        if disease_name_r: # TODO
            diseases = Disease.objects.filter(
                Q(status='a') &
                Q(disease_name__icontains=disease_name_r.lower())
            )
            
            serialized_diseases = []
            for disease in diseases:
                serializer = DiseaseSerializer(disease)
                serialized_diseases.append(serializer.data)

            serialized_diseases.append({"drugID": 0})

            return Response(serialized_diseases)

        
        diseases = Disease.objects.filter(
        Q(status='a')
        )

        serialized_diseases = []
        for disease in diseases:
            serializer = DiseaseSerializer(disease)
            serialized_diseases.append(serializer.data)

        serialized_diseases.append({"drugID": 0})

        return Response(serialized_diseases)

# добавление нового заболевания (услуги)
@swagger_auto_schema(method='post',request_body=DiseaseSerializer)
@api_view(['POST'])
@permission_classes([IsManager])
def add_disease(request, format=None):

    data = request.POST.dict()
    image_file = request.FILES.get('image')

    if image_file:
        image_data = b64encode(image_file.read()).decode('utf-8')
        data['image'] = image_data

    serializer = DiseaseSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()  
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# информация о заболевании (услуге)
@swagger_auto_schema(method='get')
@api_view(['GET'])
def get_disease(request, id, format=None):
    print("disease_id =", id)
    disease = get_object_or_404(Disease, id=id)
    if request.method == 'GET':
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data)


    


# обновление информации о заболевании (услуге)
@swagger_auto_schema(method='put', request_body=DiseaseSerializer)
@api_view(['PUT'])
@permission_classes([IsManager])
@authentication_classes([])
def update_disease(request, id, format=None):
    disease = get_object_or_404(Disease, id=id)


    image_file = request.FILES.get('image')
    if image_file:
        # Создание и сохранение изображения в формате base64
        image_data = b64encode(image_file.read()).decode('utf-8')
        disease.image = image_data

    # Обновление других полей болезни
    disease.disease_name = request.data.get('disease_name', disease.disease_name)
    disease.general_info = request.data.get('general_info', disease.general_info)
    disease.simptoms = request.data.get('simptoms', disease.simptoms)
    disease.save()
    
    return Response(status=status.HTTP_200_OK)



# удаление информации о заболевании (услуге)


@api_view(['DELETE'])
@permission_classes([IsManager])
@authentication_classes([BasicAuthentication])
def delete_disease(request, id, format=None):
    print('delete', id)
    disease = get_object_or_404(Disease, id=id)
    print(disease.status)
    disease.status="d"
    disease.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


# добавление услуги в заявку
@swagger_auto_schema(method='post', request_body=DiseaseSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_disease_to_drug(request, id):
    print("add dis to dr", id)

    if not Disease.objects.filter(id=id).exists():
        return Response(f"Заболевания с таким id не найдено")
    
    token = get_access_token(request)
    if not token:
        return Response({"error": "Access token not found"}, status=status.HTTP_401_UNAUTHORIZED)


    payload = get_jwt_payload(token)
    user_id = payload["user_id"]
    print("user", user_id)
    
    disease = Disease.objects.get(id=id)
    drug = Medical_drug.objects.filter(status=0).last()

    if drug is None:
        drug = Medical_drug.objects.create()
        drug.user_id_id = user_id
    
    drug.for_disease.add(disease)
    drug.save()

    serializer = DiseaseSerializer(drug.for_disease, many=True)
    return Response(serializer.data)
    



# список препаратов (заявок)

@swagger_auto_schema(method='get')
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_drugs(request, format=None):

    token = get_access_token(request)
    if not token:
        # return Response({"error": "Access token not found"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response('Нет токена')
    
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    # print("uuuuuuuuuser =", user_id)
    curr_user = CustomUser.objects.get(id = user_id)
    print("cccccccccccurrr uuser =", curr_user)

    start_date= request.GET.get('start_date')
    end_date= request.GET.get('end_date')
    status= request.GET.get('status')

    

    if not curr_user.is_superuser:
        drugs= Medical_drug.objects.exclude(status__in=[0]).order_by('-time_create').filter(user_id_id=user_id)
        serializer = DrugSerializer(drugs, many=True)
        return Response(serializer.data)
    else:
        drugs= Medical_drug.objects.order_by('time_create').exclude(status__in=[4, 0])
        if start_date is not None:
            drugs = drugs.filter(time_create=start_date)
        if end_date is not None:
            drugs = drugs.filter(time_finish=end_date)
        if status is not None:
            drugs = drugs.filter(status=status)


        serializer = DrugSerializer(drugs, many=True)
        return Response(serializer.data)

    

    



# информация о препарате (заявке)
@swagger_auto_schema(method='get')
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def get_drug(request, id, format=None):
    drug = get_object_or_404(Medical_drug, id=id)
   
    if request.method == 'GET':
        serializer = DrugSerializer(drug)
        return Response(serializer.data)
    


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
def delete_drug(request, id, format=None):
    drug = get_object_or_404(Medical_drug, id=id)
    drug.status = 4
    drug.save()

    return Response(status=status.HTTP_200_OK)
    

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsManager])
@authentication_classes([BasicAuthentication])
def get_users(request,format=None):

    token = get_access_token(request)
    if not token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]


    curr_user = CustomUser.objects.get(id = user_id)
    
    if curr_user.is_superuser:

        users = CustomUser.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get')
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def create_drug(request, format=None):

    token = get_access_token(request)
    if not token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]


    curr_user = CustomUser.objects.get(id = user_id)

    if not curr_user.is_superuser:
        drug = Medical_drug.objects.get(user_id_id=user_id, status=0)
        serializer = DrugSerializer(drug)


    return Response(serializer.data, status=status.HTTP_200_OK)



# удаление препарата-черновика (заявки)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def delete_entered_drug(request, format=None):
    if not Medical_drug.objects.filter(status=0).exists():
        return Response(f"Препарата со статусом 'Черновик' не существует")
    
    token = get_access_token(request)
    if not token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    curr_user = CustomUser.objects.get(id = user_id)
    print("cccccccccccurrr uuser =", curr_user)
    
    
    entered_drugs = Medical_drug.objects.get(status=0, user_id_id=user_id)
    entered_drugs.status=4
    entered_drugs.save()
    entered_drugs.for_disease.clear()
    serializer = DrugSerializer(entered_drugs, many=False)
    return Response(serializer.data)






@swagger_auto_schema(method='put', request_body=DrugSerializer)
@api_view(['PUT'])
@permission_classes([AllowAny])
@authentication_classes([])
def drug_update_status_user(request, id):

    token = get_access_token(request)
  
    if not token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    payload = get_jwt_payload(token)
    user_id = payload["user_id"]


    if not Medical_drug.objects.filter(id=id).exists():
        return Response(f"Препарата с таким id не существует")
    
    # Подключение к асинхронному веб-сервису
    
    drug = Medical_drug.objects.get(id=id)
    const_token = 'my_secret_token'
    id_test = drug.id
    # Асинхронный веб-сервис
    url = 'http://127.0.0.1:5000/api/async_calc/'
    data = {
        'id_test': id_test,
        'token': const_token
    }
    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            drug.test_status = 1
        else:
            drug.test_status = 2

        drug.save()
    except Exception as error:
        print(error)

    return Response({'message': 'Успешно обновлен статус'}, status=status.HTTP_200_OK)
    
    

    


    
@swagger_auto_schema(method='put', request_body=DrugSerializer)
@api_view(['PUT'])
@permission_classes([IsManager])
@authentication_classes([])
def drug_update_status_admin(request, id):
    if not Medical_drug.objects.filter(id=id).exists():
        return Response(f"Препарата с таким id не существует")
    
    STATUSES = [0, 1, 2, 3, 4]
    request_st = request.data["status"]

    if request_st not in STATUSES:
        return Response("Статус не корректен")
    
    drug = Medical_drug.objects.get(id=id)
    drug_st = drug.status
    print("drug_st =", drug_st)

    if request_st == 2 or request_st == 3:
        drug.status = request_st
        drug.save()

        serializer = DrugSerializer(drug, many=False)
        return Response(serializer.data)
    else:
        return Response("Изменение статуса невозможно")
    

# удаление заболевания из связанного с ним препарата (из м-м)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_disease_from_drug(request, disease_id_r, drug_id_r, format=None):
    print('delete')
    if not Disease.objects.filter(id=disease_id_r).exists():
        return Response(f"Заболевания с таким id не существует")
    if not Medical_drug.objects.filter(id=drug_id_r).exists():
        return Response(f"Препарата с таким id не существует")
    
    
    disease = Disease.objects.get(id=disease_id_r)
    print("disease =", disease)
    drug = Medical_drug.objects.get(id=drug_id_r)
    print("drug =", drug)
    if drug.for_disease.exists():
        drug.for_disease.remove(disease)
        drug.save()

        return Response(f"Удаление выполнено")
    else:
        return Response(f"Объектов для удаления не найдено", status = status.HTTP_404_NOT_FOUND)



# Connect to our Redis instance
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)




@swagger_auto_schema(method='put')
@api_view(['PUT'])
@permission_classes([AllowAny])
def async_result(request, format=None):
    try:
        # Преобразуем строку в объект Python JSON
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        const_token = 'my_secret_token'

        if const_token != json_data['token']:
            return Response(data={'message': 'Ошибка, токен не соответствует'}, status=status.HTTP_403_FORBIDDEN)

       
        try:
            # Выводит конкретную заявку создателя
            drug = get_object_or_404(Medical_drug, id=json_data['id_test'])
            drug.test_status = json_data['test_status']
          
            drug.save()
            data_json = {
                'id': drug.id,
                'test_status': drug.get_test_status_display_word(),
                'status': drug.get_grug_display_word()
            }
            return Response(data={'message': 'Статус тестированя успешно обновлен', 'data': data_json},
                            status=status.HTTP_200_OK)
        except ValueError:
            return Response({'message': 'Недопустимый формат преобразования'}, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {e}')
        return Response(data={'message': 'Ошибка декодирования JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
