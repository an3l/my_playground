# Generated by Django 2.2.1 on 2019-05-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tehnicka', '0014_auto_20190521_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredmetIspis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod', models.CharField(default='MM', max_length=2)),
                ('naziv', models.CharField(max_length=64)),
            ],
        ),
    ]