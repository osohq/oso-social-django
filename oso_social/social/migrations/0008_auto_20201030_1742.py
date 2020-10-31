# Generated by Django 3.1.1 on 2020-10-30 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social", "0007_auto_20201023_2030"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="role",
            name="created_by",
        ),
        migrations.AddField(
            model_name="role",
            name="custom",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="permission",
            name="resource",
            field=models.IntegerField(choices=[(0, "post")]),
        ),
    ]
