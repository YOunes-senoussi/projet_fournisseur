# Generated by Django 4.1.7 on 2023-03-20 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0005_storefavclients_store_fav_clients_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientsFavStores",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clientfavstores",
                        related_query_name="clientfavstore",
                        to="API.client",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="API.store"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="client",
            name="fav_stores",
            field=models.ManyToManyField(
                through="API.ClientsFavStores", to="API.store"
            ),
        ),
        migrations.AddConstraint(
            model_name="clientsfavstores",
            constraint=models.UniqueConstraint(
                fields=("client_id", "store_id"), name="unique_client_store"
            ),
        ),
    ]
