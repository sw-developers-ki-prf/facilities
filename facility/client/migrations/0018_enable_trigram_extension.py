# Generated by Django 4.2 on 2023-04-25 20:21
from django.contrib.postgres.operations import TrigramExtension

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0017_alter_attachment_file_alter_contact_photo_and_more"),
    ]

    operations = [
        TrigramExtension(),
    ]
