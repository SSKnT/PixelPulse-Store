# Generated by Django 5.0.2 on 2024-05-30 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_order_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_quantities',
            field=models.JSONField(default=dict),
        ),
    ]