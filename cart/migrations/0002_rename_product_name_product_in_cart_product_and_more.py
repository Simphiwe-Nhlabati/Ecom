# Generated by Django 5.2.3 on 2025-07-03 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_in_cart',
            old_name='product_name',
            new_name='product',
        ),
        migrations.AddField(
            model_name='product_in_cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
