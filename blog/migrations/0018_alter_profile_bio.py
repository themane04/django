# Generated by Django 5.0.2 on 2024-02-24 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_delete_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]