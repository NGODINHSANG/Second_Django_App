# Generated by Django 3.2.2 on 2021-07-02 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_order_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
