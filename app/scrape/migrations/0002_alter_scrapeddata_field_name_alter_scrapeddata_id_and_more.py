# Generated by Django 4.2.16 on 2024-10-30 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
        ('scrape', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapeddata',
            name='field_name',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='scrapeddata',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='scrapeddata',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.page'),
        ),
    ]
