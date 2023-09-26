from django.db import models

# Create your models here.
from django.db import models


class Sphere(models.Model):
    sphere_id = models.IntegerField(primary_key=True)
    sphere_name = models.CharField(max_length=100)

    def __str__(self):
        return self.sphere_name

    class Meta:
        managed = False
        verbose_name_plural = 'Сфера применения'


class Disease(models.Model):
    disease_id = models.IntegerField(primary_key=True)
    disease_name = models.CharField(max_length=150)
    general_info = models.CharField(max_length=255)
    simptoms = models.CharField(max_length=255)
    sphere_id = models.OneToOneField(Sphere, on_delete=models.CASCADE)
    image = models.TextField(default='')

    

    STATUSES = [
        ('a', 'active'),
        ('d', 'delited')
    ]
    status = models.CharField(max_length=1, choices=STATUSES)

    def __str__(self):
        return self.disease_name

    class Meta:
        verbose_name_plural = 'Заболевания'


class Medical_drug(models.Model):
    drug_id =models.IntegerField(primary_key=True)
    drug_name = models.CharField(max_length=150)
    sphere_id = models.ForeignKey('Sphere', on_delete=models.CASCADE)
    # автоматом ставим время только при изменении объекта, а не при создании
    time_create = models.DateTimeField(auto_now=True) 
    time_form = models.DateTimeField(auto_now=True, auto_now_add=False) 
    time_finish = models.DateTimeField(auto_now=True, auto_now_add=False)
    price = models.IntegerField(default=0)
    for_disease = models.ManyToManyField('Disease', through='DiseaseDrug')
    sphere_id = models.OneToOneField(Sphere, on_delete=models.CASCADE)
    STATUSES = [
        ('e', 'entered'), # введён
        ('o', 'in operation'), # в работе
        ('f', 'finished'), # завершён
        ('c', 'cancelled'), # отменён 
        ('d', 'deleted') # удалён
    ]
    status = models.CharField(max_length=1, choices=STATUSES)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.drug_name
    
    

    class Meta:
        verbose_name_plural = 'Медицинские препараты'
    



class DiseaseDrug(models.Model):
    disease_id = models.ForeignKey(Disease, on_delete=models.CASCADE)
    drug_id = models.ForeignKey(Medical_drug, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = 'Заболевание-препарат'


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user_name

    class Meta:
        managed = False
        verbose_name_plural = 'Пользователи'


class User_test(models.Model):
    user = models.IntegerField(primary_key=True)
   
