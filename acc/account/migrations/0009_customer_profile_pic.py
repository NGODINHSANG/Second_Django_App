# Generated by Django 3.2.2 on 2021-07-06 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
