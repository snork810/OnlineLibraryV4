# Generated by Django 5.1 on 2024-08-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NoModeratedBooksModel",
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
                ("title", models.CharField(max_length=80, verbose_name="Название")),
                (
                    "summary",
                    models.TextField(max_length=10000, verbose_name="Аннотация"),
                ),
                ("pages", models.IntegerField(verbose_name="Количество страниц")),
                (
                    "txt",
                    models.FileField(
                        upload_to="texts/nomoderated/", verbose_name="Загрузите файл"
                    ),
                ),
                ("author", models.CharField(max_length=50, verbose_name="Автор")),
                ("category", models.CharField(max_length=80, verbose_name="Категория")),
            ],
            options={
                "verbose_name": "Не модерированное",
            },
        ),
    ]