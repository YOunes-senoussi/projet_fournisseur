# Generated by Django 4.1.6 on 2023-02-09 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Client",
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
                ("full_name", models.CharField(blank=True, max_length=100, null=True)),
                ("shop_name", models.CharField(blank=True, max_length=100, null=True)),
                ("phone_number", models.IntegerField(blank=True, null=True)),
                ("password", models.CharField(blank=True, max_length=100, null=True)),
                ("e_mail", models.CharField(blank=True, max_length=100, null=True)),
                ("wilaya", models.CharField(blank=True, max_length=100, null=True)),
                ("commune", models.CharField(blank=True, max_length=100, null=True)),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                ("created_at", models.IntegerField(blank=True, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Coupon",
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
                ("string", models.CharField(blank=True, max_length=100, null=True)),
                ("discount", models.IntegerField(blank=True, null=True)),
                (
                    "coupon_type",
                    models.CharField(
                        choices=[
                            ("Product", "Product"),
                            ("Category", "Category"),
                            ("All", "All"),
                        ],
                        max_length=100,
                    ),
                ),
                ("target_id", models.IntegerField(blank=True, null=True)),
                ("max_nbr_uses", models.IntegerField(blank=True, null=True)),
                ("created_at", models.IntegerField(blank=True, null=True)),
                ("is_active", models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                ("created_at", models.IntegerField()),
                ("description", models.TextField()),
                ("total_price", models.FloatField()),
                (
                    "client_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.client",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PackType",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="UsedCoupon",
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
                    "client_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.client",
                    ),
                ),
                (
                    "coupon_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.coupon",
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.order",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Store",
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
                ("full_name", models.CharField(blank=True, max_length=100, null=True)),
                ("store_name", models.CharField(blank=True, max_length=100, null=True)),
                ("image_url", models.CharField(blank=True, max_length=100, null=True)),
                ("phone_number", models.IntegerField(blank=True, null=True)),
                ("password", models.CharField(blank=True, max_length=100, null=True)),
                ("e_mail", models.CharField(blank=True, max_length=100, null=True)),
                ("wilaya", models.CharField(blank=True, max_length=100, null=True)),
                ("commune", models.CharField(blank=True, max_length=100, null=True)),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                ("created_at", models.IntegerField(blank=True, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("fav_clients_list", models.ManyToManyField(to="API.client")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("brand", models.CharField(blank=True, max_length=100, null=True)),
                ("price", models.FloatField()),
                ("image_url", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("nbr_units", models.IntegerField(blank=True, null=True)),
                ("created_at", models.IntegerField(blank=True, null=True)),
                ("is_available", models.BooleanField(blank=True, null=True)),
                ("discount", models.IntegerField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.category",
                    ),
                ),
                (
                    "pack_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.packtype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.IntegerField()),
                ("price", models.FloatField()),
                (
                    "order_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.order",
                    ),
                ),
                (
                    "product_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="store_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="API.store",
            ),
        ),
        migrations.CreateModel(
            name="Group",
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
                ("name", models.CharField(max_length=100)),
                ("created_at", models.IntegerField()),
                ("clients_list", models.ManyToManyField(to="API.client")),
                (
                    "store_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="API.store",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="coupon",
            name="store_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="API.store",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="fav_stores_list",
            field=models.ManyToManyField(to="API.store"),
        ),
    ]