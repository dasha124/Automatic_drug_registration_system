from django.contrib import admin

from list_of_diseases.models import Disease, Medical_drug, Sphere, DiseaseDrug, User


admin.site.register(Disease)
admin.site.register(Medical_drug)
admin.site.register(Sphere)
admin.site.register(DiseaseDrug)
admin.site.register(User)