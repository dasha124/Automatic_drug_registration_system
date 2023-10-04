# Generated by Django 4.2.4 on 2023-10-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_of_diseases', '0002_alter_disease_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='disease_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='medical_drug',
            name='drug_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sphere',
            name='sphere_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
