# Generated by Django 4.0 on 2023-02-19 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0015_alter_coupon_store_alter_group_store_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupons', related_query_name='coupon', to='API.store'),
        ),
        migrations.AlterField(
            model_name='group',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', related_query_name='group', to='API.store'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', related_query_name='order', to='API.client'),
        ),
        migrations.AlterField(
            model_name='order',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', related_query_name='order', to='API.store'),
        ),
        migrations.AlterField(
            model_name='ordercoupon',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordercoupons', related_query_name='ordercoupon', to='API.client'),
        ),
        migrations.AlterField(
            model_name='ordercoupon',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordercoupons', related_query_name='ordercoupon', to='API.coupon'),
        ),
        migrations.AlterField(
            model_name='ordercoupon',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordercoupons', related_query_name='ordercoupon', to='API.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitems', related_query_name='orderitem', to='API.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitems', related_query_name='orderitem', to='API.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', related_query_name='product', to='API.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pack_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', related_query_name='product', to='API.packtype'),
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', related_query_name='product', to='API.store'),
        ),
    ]