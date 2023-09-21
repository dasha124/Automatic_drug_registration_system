from django.db import models



class Disease(models.Model):
    disease_name = models.CharField(max_length=150)
    #image = 
    general_info = models.CharField(max_length=255)
    simptoms = models.CharField(max_length=255)
    sphere_id = models.ForeignKey('Sphere', on_delete=models.PROTECT)

    STATUSES = [
        ('a', 'active'),
        ('d', 'delited')
    ]
    status = models.CharField(max_length=1, choices=STATUSES)
    


class Medical_drug(models.Model):
    drug_name = models.CharField(max_length=150)
    sphere_id = models.ForeignKey('Sphere', on_delete=models.PROTECT)
    # автоматом ставим время только при изменении объекта, а не при создании
    time_create = models.DateTimeField(auto_now=True) 
    time_form = models.DateTimeField(auto_now=True, auto_now_add=False) 
    time_finish = models.DateTimeField(auto_now=True, auto_now_add=False)

    STATUSES = [
        ('e', 'entered'), # введён
        ('o', 'in operation'), # в работе
        ('f', 'finished'), # завершён
        ('c', 'cancelled'), # отменён 
        ('d', 'deleted') # удалён
    ]
    status = models.CharField(max_length=1, choices=STATUSES)
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)


    class DiseaseDrug(models.Model):
        disease_id = models.ForeignKey('Disease', on_delete=models.PROTECT)
        drug_id = models.ForeignKey('Medical_drug', on_delete=models.PROTECT)


class Sphere(models.Model):
    sphere_name = models.CharField(max_length=100)


class User(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)






    



