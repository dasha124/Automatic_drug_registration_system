from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import date

services =[
    {'title': 'Герпес', 'aspect': 'Инфекционные болезни', 'id': 0, 'src': 'https://familydoctor.ru/upload/medialibrary/f96/prostuda_na_gubah.jpg', \
        'text':'Герпес – распространенная вирусная инфекция, \
                 которая характеризуется образованием на коже маленьких сгруппированных пузырьков, заполненных жидкостью.',
        'simp':['повышение температуры тела', 'болезненность в горле', 'головная боль', 'мышечная боль',\
                'увеличение лимфатических узлов в зоне высыпаний']},

    {'title': 'Нарушения сердечного ритма','aspect': 'Кардиология','id': 1, 'src': 'https://img.freepik.com/premium-vector/heart-cardiogram-isolated-on-white_97886-1185.jpg',
        'text': 'Нарушения сердечного ритма – собирательный диагноз различных \
            тахи и брадиаритмий, в том числе и различных патологических процессов,\
            связанных с проводящей системой сердца.',
        'simp':['учащенное сердцебиение', 'резкие перебои ритма в сердце','снижение артериального давления',\
                'боли в груди', 'слабость и быстрая утомляемость', 'нехватка воздуха'] },
    {'title': 'Сахарный диабет', 'aspect': 'Эндокринология','id': 2, \
     'src': 'https://www.smclinic.ru/upload/iblock/fe6/s98g9jazsj9nvello5yf6pa66lgcwm54.png', \
     'text': 'Сахарный диабет относится к группе эндокринных заболеваний. \
            Патология развивается при нарушении выработки или действия на ткани\
         инсулина — гормона островкового аппарата поджелудочной железы, способствующего усвоению глюкозы. ',
    'simp':['мучительная сухость во рту, ощущение набухания слизистой ротовой полости',\
                'изменение массы тела, жажда, повышенное мочеиспускание, постоянное чувство голода;',
                'общие неспецифические жалобы — упадок сил, утомляемость при незначительных нагрузках, сонливость, мышечная слабость;']},
]

def GetServices(request):
    return render(request, 'services.html', {'services': services})


def GetService(request, id):
    for s in services:
        if s['id']==id:
            return render(request, 'service.html',{'s': s})


def GetQuery(request):
    query = request.GET.get('query', '')
    #print("__QUERY__ =", query, type(query))
    new_services = []
    for service in services:
        if query.lower() in service["title"].lower():
            new_services.append(service)

    if len(new_services)>0:
        return render(request, 'services.html',{'services': new_services})
    else:
        return render(request, 'services.html', {'services': services})