# Generated by Django 3.2 on 2023-01-01 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_alter_cafe_wordcloud_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='customers',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='customers IMAGE'),
        ),
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='dessert',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='dessert IMAGE'),
        ),
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='drink',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='drink IMAGE'),
        ),
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='interior',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='interior IMAGE'),
        ),
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='parking',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='parking IMAGE'),
        ),
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='price',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='service',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='service IMAGE'),
        ),
        migrations.AlterField(
            model_name='cafe_wordcloud',
            name='view',
            field=models.ImageField(blank=True, null=True, upload_to='owner/', verbose_name='view IMAGE'),
        ),
    ]
