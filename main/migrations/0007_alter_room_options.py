# Generated by Django 5.1.5 on 2025-03-18 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_alter_message_options_alter_room_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="room",
            options={"ordering": ["-updated", "-created"]},
        ),
    ]
