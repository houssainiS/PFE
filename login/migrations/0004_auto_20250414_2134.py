# Generated by Django 3.2.13 on 2025-04-14 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20250323_2038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='plan',
            field=models.CharField(choices=[('free', 'Free'), ('pro', 'Pro'), ('premium', 'Premium')], default='free', max_length=10),
        ),
    ]
