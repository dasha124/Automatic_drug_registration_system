from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import date
from django.db import connection

from list_of_diseases.models import Disease, Medical_drug, DiseaseDrug, User

def DiseasesList(request):
    query = request.GET.get('query', '')

    search_diseases = Disease.objects.filter(disease_name__icontains=query, status='a')
    
    search_diseases_list = list(search_diseases)
    
    return render(request, 'diseases.html', {'data': search_diseases_list})

    

def GetDisease(request, id):
    s = Disease.objects.get(disease_id=id).simptoms.split(',')
    return render(request, 'disease.html', {'data': { 
        'disease': Disease.objects.get(disease_id=id),
        'simptoms': s
        }  
    })



def Delete(self, id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE list_of_diseases_disease SET status='d' WHERE disease_id = %s", [id])
    return redirect("/")
