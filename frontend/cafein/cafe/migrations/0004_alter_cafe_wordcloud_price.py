# Generated by Django 3.2 on 2023-01-01 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0003_cafe_wordcloud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='price',
            field=models.ImageField(blank=True, null=True, upload_to='owner', verbose_name='price'),
        ),
    ]
