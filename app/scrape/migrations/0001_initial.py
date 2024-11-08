
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_value', models.TextField()),
                ('field_value_meta', models.TextField()),  # JSON values
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('page', models.ForeignKey(on_delete=models.CASCADE, related_name='scraped_data', to='pages.Page')),
            ],
            options={
                'db_table': 'scraped_data',
                'verbose_name': 'Scraped Data',
                'verbose_name_plural': 'Scraped Data',
            },
        ),
    ]
