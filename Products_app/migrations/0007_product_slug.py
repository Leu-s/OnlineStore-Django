# Generated by Django 3.1.5 on 2021-02-10 15:19

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Products_app', '0006_auto_20210205_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title'),
        ),
    ]
