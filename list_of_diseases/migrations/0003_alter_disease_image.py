# Generated by Django 4.2.4 on 2023-12-07 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_of_diseases', '0002_rename_disease_id_disease_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='image',
            field=models.TextField(default=''),
        ),
    ]
