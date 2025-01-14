# Generated by Django 5.1.4 on 2025-01-14 16:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
            },
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ("-created_at",)},
        ),
    ]
