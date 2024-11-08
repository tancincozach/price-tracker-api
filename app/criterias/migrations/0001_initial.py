# Generated by Django 4.2.16 on 2024-10-09 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Criterias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('html_tag', models.CharField(max_length=50)),
                ('css_selector', models.CharField(max_length=255)),
                ('meta', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Criteria',
                'verbose_name_plural': 'Criterias',
                'db_table': 'criterias',
            },
        ),
    ]
