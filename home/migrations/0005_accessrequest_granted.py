# Generated by Django 5.1.5 on 2025-01-27 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_cartobject_sizedata_remove_product_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessrequest',
            name='granted',
            field=models.BooleanField(default=False),
        ),
    ]
