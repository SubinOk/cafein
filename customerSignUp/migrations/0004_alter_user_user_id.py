# Generated by Django 3.2 on 2022-12-06 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerSignUp', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.EmailField(max_length=254),
        ),
    ]
