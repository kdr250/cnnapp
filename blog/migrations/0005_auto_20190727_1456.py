# Generated by Django 2.2.3 on 2019-07-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190727_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='uploads', verbose_name='写真'),
        ),
    ]
