from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import date
from django.db import connection

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from list_of_diseases.serializers import *
from list_of_diseases.models import *
from rest_framework.decorators import api_view
from operator import itemgetter



# список заболеваний (услуг)
@api_view(['GET'])
def get_diseases(request, format=None):
    print('get_1')
    disease_name_r = request.GET.get('disease_name')
    print('disease_name_r =', disease_name_r)
    diseases = Disease.objects.filter(status='a')

    if disease_name_r:
        diseases = Disease.objects.filter(
            Q(status='a') &
            Q(disease_name__icontains=disease_name_r.lower())
        )
        serializer = DiseaseSerializer(diseases, many=True )

        return Response(serializer.data)
    
    serializer = DiseaseSerializer(diseases, many=True )
    serialized_data = serializer.data


    return Response(serializer.data)


# список заболеваний (услуг) с фильтром поиска 
@api_view(['GET'])
def get_found_diseases(request, format=None):
    print('get')
    disease_name_r = request.data.get('disease_name')
    sphere_r = request.data.get('sphere')
    print("disease_name_r =", disease_name_r, sphere_r)

    diseases = Disease.objects.filter(status='a')

    if disease_name_r:
        diseases = diseases.filter(disease_name=disease_name_r)
        serializer = DiseaseSerializer(diseases, many=True )
   
        return Response(serializer.data)

    if sphere_r:
        spheres = Sphere.objects.get(sphere_name=sphere_r)
        diseases = diseases.filter(sphere_id=spheres.sphere_id)
        serializer = DiseaseSerializer(diseases, many=True )
   
        return Response(serializer.data)




# добавление нового заболевания (услуги)
@api_view(['POST'])
def post_disease(request, format=None):
    print('post')
    serializer = DiseaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        diseases = Disease.objects.filter(status='a')
        serializer = DiseaseSerializer(diseases, many=True )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# информация о заболевании (услуге)
@api_view(['GET'])
def get_disease(request, id, format=None):
    print("disease_id =", id)
    disease = get_object_or_404(Disease, disease_id=id)
    if request.method == 'GET':
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data)
    


# обновление информации о заболевании (услуге)
@api_view(['PUT'])
def put_disease(request, id, format=None):
    disease = get_object_or_404(Disease, disease_id=id)
    serializer = DiseaseSerializer(disease, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# удаление информации о заболевании (услуге)
@api_view(['DELETE'])
def delete_disease(request, id, format=None):
    print('delete')
    disease = get_object_or_404(Disease, disease_id=id)
    disease.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# добавление услуги в заявку
@api_view(['POST'])
def add_disease_to_drug(request, id):
    if not Disease.objects.filter(disease_id=id).exists():
        return Response(f"Заболевания с таким id не найдено")
    
    disease = Disease.objects.get(disease_id=id)
    drug = Medical_drug.objects.filter(status='e').last()

    if drug is None:
        drug = Medical_drug.objects.create()
    
    drug.for_disease.add(disease)
    drug.save()

    serializer = DiseaseSerializer(drug.for_disease, many=True)
    return Response(serializer.data)
    

# список препаратов (заявок)
@api_view(['GET'])
def get_drugs(request, format=None):
    print('get')
    drugs= Medical_drug.objects.order_by('-time_create').filter(status='e')
    #drugs= Medical_drug.objects.all()
    serializer = DrugSerializer(drugs, many=True)

    return Response(serializer.data)

    

# информация о препарате (заявке)
@api_view(['GET'])
def get_drug(request, id, format=None):
    drug = get_object_or_404(Medical_drug, drug_id=id)

    if request.method == 'GET':
        serializer = DrugSerializer(drug)
        return Response(serializer.data)
    

# изменение информации о препарате (заявке)
@api_view(['PUT'])
def update_drug(request, id, format=None):
    drug = get_object_or_404(Medical_drug, drug_id=id)
    serializer = DrugSerializer(drug, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# удаление информации о препарате (заявке)
@api_view(['DELETE'])
def delete_drug(request, id, format=None):
    print('delete')
    drug = get_object_or_404(Medical_drug, drug_id=id)
    drug.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# удаление введенного препарата (заявки)
@api_view(['DELETE'])
def delete_entered_drug(request, format=None):
    if not Medical_drug.objects.filter(status='e').exists():
        return Response(f"Препарата со статусом 'Черновик' не существует")
    
    entered_drugs = Medical_drug.objects.filter(status='e')
    for drug in entered_drugs:
        drug.delete()
    serializer = DrugSerializer(entered_drugs, many=False)
    return Response(serializer.data)





@api_view(['PUT'])
def drug_update_status_user(request, id):
    if not Medical_drug.objects.filter(drug_id=id).exists():
        return Response(f"Препарата с таким id не существует")
    
    STATUSES = ['e', 'o', 'f', 'c', 'd']
    request_st = request.data["status"]

    if request_st not in STATUSES:
        return Response("Статус не корректен")
    
    drug = Medical_drug.objects.get(drug_id=id)
    drug_st = drug.status
    print("drug_st =", drug_st)

    if drug_st == 'd':
        return Response("Изменение статуса невозможно")
    
    if request_st == 'd':
        drug.status = request_st
        drug.save()

        serializer = DrugSerializer(drug, many=False)
        return Response(serializer.data)
    else:
        return Response("Изменение статуса невозможно")
    

    
@api_view(['PUT'])
def drug_update_status_admin(request, id):
    if not Medical_drug.objects.filter(drug_id=id).exists():
        return Response(f"Препарата с таким id не существует")
    
    STATUSES = ['e', 'o', 'f', 'c', 'd']
    request_st = request.data["status"]

    if request_st not in STATUSES:
        return Response("Статус не корректен")
    
    drug = Medical_drug.objects.get(drug_id=id)
    drug_st = drug.status
    print("drug_st =", drug_st)

    if request_st == 'f' or request_st == 'c':
        drug.status = request_st
        drug.save()

        serializer = DrugSerializer(drug, many=False)
        return Response(serializer.data)
    else:
        return Response("Изменение статуса невозможно")
    

# удаление заболевания из связанного с ним препарата (из м-м)
@api_view(['DELETE'])
def delete_disease_from_drug(request, disease_id_r, drug_id_r, format=None):
    print('delete')
    if not Disease.objects.filter(disease_id=disease_id_r).exists():
        return Response(f"Заболевания с таким id не существует")
    if not Medical_drug.objects.filter(drug_id=drug_id_r).exists():
        return Response(f"Препарата с таким id не существует")
    
    
    disease = Disease.objects.get(disease_id=disease_id_r)
    print("disease =", disease)
    drug = Medical_drug.objects.get(drug_id=drug_id_r)
    print("drug =", drug)
    if drug.for_disease.exists():
        print("drug_disease type =", drug.for_disease.get())
        drug.for_disease.remove(disease)
        drug.save()

        return Response(f"Удаление выполнено")
    else:
        return Response(f"Объектов для удаления не найдено", status = status.HTTP_404_NOT_FOUND)

    
    
    
