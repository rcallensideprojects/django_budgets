# Generated by Django 5.0.4 on 2024-04-21 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_transaction_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
