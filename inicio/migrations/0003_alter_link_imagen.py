# Generated by Django 5.1.3 on 2024-11-09 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inicio", "0002_link_delete_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="Imagen",
            field=models.ImageField(upload_to="inicio/images/"),
        ),
    ]