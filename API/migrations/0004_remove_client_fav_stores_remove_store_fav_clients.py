# Generated by Django 4.1.7 on 2023-03-20 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0003_cart_items"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="client",
            name="fav_stores",
        ),
        migrations.RemoveField(
            model_name="store",
            name="fav_clients",
        ),
    ]
