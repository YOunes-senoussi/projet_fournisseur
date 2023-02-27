# Generated by Django 4.1.7 on 2023-02-25 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0020_cart_remove_order_error_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="client",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart",
                related_query_name="cart",
                to="API.client",
            ),
        ),
    ]
