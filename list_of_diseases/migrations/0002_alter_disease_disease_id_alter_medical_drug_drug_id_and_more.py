# Generated by Django 4.2.4 on 2023-10-14 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list_of_diseases', '0001_initial'),
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
            model_name='medical_drug',
            name='sphere_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='list_of_diseases.sphere'),
        ),
    ]