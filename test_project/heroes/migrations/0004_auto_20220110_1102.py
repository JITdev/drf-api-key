# Generated by Django 3.2.11 on 2022-01-10 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("heroes", "0003_alter_hero_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="heroapikey",
            name="hashed_key",
            field=models.CharField(editable=False, max_length=150),
        ),
        migrations.AlterField(
            model_name="heroapikey",
            name="id",
            field=models.CharField(
                editable=False,
                max_length=150,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
