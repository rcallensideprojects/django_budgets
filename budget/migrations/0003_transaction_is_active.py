# Generated by Django 5.0.4 on 2024-04-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
