# Generated by Django 2.2.1 on 2019-05-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tehnicka', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucenik',
            name='JMBG',
            field=models.IntegerField(null=True),
        ),
    ]