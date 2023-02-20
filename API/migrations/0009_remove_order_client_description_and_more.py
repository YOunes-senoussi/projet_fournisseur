# Generated by Django 4.0 on 2023-02-14 22:36

import API.more_functions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_rename_description_order_client_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='client_description',
        ),
        migrations.RemoveField(
            model_name='order',
            name='store_description',
        ),
        migrations.AddField(
            model_name='order',
            name='error_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.IntegerField(blank=True, default=API.more_functions.get_now_stamp, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='created_at',
            field=models.IntegerField(blank=True, default=API.more_functions.get_now_stamp, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='created_at',
            field=models.IntegerField(blank=True, default=API.more_functions.get_now_stamp, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.IntegerField(blank=True, default=API.more_functions.get_now_stamp, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.IntegerField(blank=True, default=API.more_functions.get_now_stamp, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='created_at',
            field=models.IntegerField(blank=True, default=API.more_functions.get_now_stamp, null=True),
        ),
    ]
