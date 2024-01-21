# Generated by Django 5.0 on 2023-12-29 09:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_of_diseases', '0008_medical_drug_test_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'managed': True},
        ),
        migrations.AddField(
            model_name='medical_drug',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moderator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medical_drug',
            name='status',
            field=models.IntegerField(choices=[(0, 'Черновик'), (1, 'Сформирована'), (2, 'Завершён'), (3, 'Отменён'), (4, 'Удалён')], default=0),
        ),
        migrations.AlterField(
            model_name='medical_drug',
            name='time_create',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='medical_drug',
            name='time_finish',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='medical_drug',
            name='time_form',
            field=models.DateField(auto_now=True),
        ),
    ]