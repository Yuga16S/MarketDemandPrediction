# Generated by Django 4.2.5 on 2023-09-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marketdemandpredictionapp", "0004_alter_crops_crop_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crops",
            name="crop_code",
            field=models.PositiveIntegerField(),
        ),
    ]