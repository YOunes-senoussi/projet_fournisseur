# Generated by Django 4.1.7 on 2023-03-06 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0006_remove_cartitem_positive_quantity_2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="couponcount",
            name="count",
            field=models.IntegerField(default=1),
        ),
    ]
