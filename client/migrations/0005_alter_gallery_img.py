# Generated by Django 3.2 on 2023-03-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_gallery_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='gallery/'),
        ),
    ]
