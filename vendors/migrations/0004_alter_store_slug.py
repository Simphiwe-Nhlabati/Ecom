# Generated by Django 5.2.1 on 2025-06-16 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_alter_product_image_alter_product_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
