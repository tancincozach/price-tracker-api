# Generated by Django 4.2.16 on 2024-11-01 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '__first__'),
        ('criterias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterias',
            name='website',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='criterias', to='websites.website'),
        ),
    ]
