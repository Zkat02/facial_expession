# Generated by Django 4.1.3 on 2022-12-12 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recognition_app", "0003_alter_calculation_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="calculation",
            name="calculation_name",
            field=models.CharField(
                default="image_1670883289714", max_length=20, verbose_name="image name"
            ),
        ),
    ]
