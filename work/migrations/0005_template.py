# Generated by Django 3.2.13 on 2025-03-27 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0004_alter_generatedwebsite_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('theme', models.CharField(max_length=100)),
                ('code', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
