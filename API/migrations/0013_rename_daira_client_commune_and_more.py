# Generated by Django 4.0 on 2023-02-18 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0012_ordercoupon_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='daira',
            new_name='commune',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='daira',
            new_name='commune',
        ),
    ]