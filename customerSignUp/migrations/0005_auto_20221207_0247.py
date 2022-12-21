# Generated by Django 3.2 on 2022-12-06 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerSignUp', '0004_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]