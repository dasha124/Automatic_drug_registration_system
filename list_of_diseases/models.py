from django.db import models

# Create your models here.
from django.db import models



class Disease(models.Model):
    disease_id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=150)
    general_info = models.CharField(max_length=255)
    simptoms = models.CharField(max_length=255)
    sphere_id = models.ForeignKey(Sphere, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='list_of_diseases/static/images', blank=True, null=True)

    STATUSES = [
        ('a', 'active'),
        ('d', 'delited')
    ]
    status = models.CharField(max_length=1, choices=STATUSES)

    def __str__(self):
        return self.disease_name

    class Meta:
        managed = True
        verbose_name_plural = 'Заболевания'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user_name

    class Meta:
        managed = True
        verbose_name_plural = 'Пользователи'


class Medical_drug(models.Model):
    drug_id =models.AutoField(primary_key=True)
    drug_name = models.CharField(max_length=150)
    time_create = models.DateTimeField(auto_now_add=True) 
    time_form = models.DateTimeField(auto_now=True) 
    time_finish = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0)
    for_disease = models.ManyToManyField(Disease, through='DiseaseDrug')
    STATUSES = [
        (0, 'Черновик'), 
        (1, 'Сформирована'), 
        (2, 'Завершёна'), 
        (3, 'Отменёна'), 
        (4, 'Удалёна') 
    ]
    status = models.CharField(max_length=1, choices=STATUSES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.drug_name
    
    class Meta:
        managed = True
        verbose_name_plural = 'Медицинские препараты'
    


class DiseaseDrug(models.Model):
    disease_id = models.ForeignKey(Disease, on_delete=models.CASCADE)
    drug_id = models.ForeignKey(Medical_drug, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.disease_id.disease_name}{self.drug_id.drug_name}"

    class Meta:
        managed = True
        verbose_name_plural = 'Заболевание-препарат'



   
