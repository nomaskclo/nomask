# Generated by Django 5.1.5 on 2025-01-30 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_product_discount_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_percentage',
        ),
    ]
