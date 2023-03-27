# [Mostly] generated by Django 4.1.3 on 2023-03-23 21:59
# The CreateExtension calls to postgis and postgis_raster were made separately, 
# and are necessary for RasterField (in AttributeRaster)

import django.contrib.gis.db.models.fields
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        CreateExtension('postgis'),
        CreateExtension('postgis_raster'),
        migrations.CreateModel(
            name="Attribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("attribute_name", models.CharField(max_length=120)),
                ("display_name", models.CharField(max_length=120, null=True)),
                ("raster_name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="AttributeRaster",
            fields=[
                ("rid", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.TextField(null=True)),
                (
                    "raster",
                    django.contrib.gis.db.models.fields.RasterField(
                        null=True, srid=9822
                    ),
                ),
            ],
        ),
    ]