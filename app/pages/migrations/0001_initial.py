# Generated by Django 4.2.16 on 2024-10-30 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('websites', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('scraped', 'Scraped'), ('error', 'Error')], default='pending', max_length=10)),
                ('last_scraped', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('web', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='websites.website')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'db_table': 'pages',
            },
        ),
    ]
