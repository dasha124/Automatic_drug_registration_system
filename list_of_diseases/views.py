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
    
    print(query)

    search_diseases = Disease.objects.filter(disease_name__icontains=query)

    search_diseases_list = list(search_diseases)

    # Передадим отфильтрованные объекты в шаблон для отображения
    return render(request, 'geographical_objects.html', {'data': filtered_objects_list})
    
   

    if len(search_diseases)>0:
        return render(request, 'diseases.html', {'data': {
        'diseases': search_diseases
    }})
    else:
        return render(request, 'diseases.html', {'data': {
        'diseases': Disease.objects.all()
    }})

    

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
