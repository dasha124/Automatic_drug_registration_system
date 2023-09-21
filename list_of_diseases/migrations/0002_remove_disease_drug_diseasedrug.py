# Generated by Django 4.2.4 on 2023-09-20 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list_of_diseases', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disease',
            name='drug',
        ),
        migrations.CreateModel(
            name='DiseaseDrug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='list_of_diseases.disease')),
                ('drug_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='list_of_diseases.medical_drug')),
            ],
        ),
    ]
