# Generated by Django 4.2.5 on 2023-09-18 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(max_length=255, unique=True)),
                ('ep_description', models.TextField()),
                ('ep_hours', models.TextField()),
                ('ep_education', models.TextField()),
                ('ep_license', models.TextField()),
                ('ep_career', models.TextField()),
                ('ep_product', models.JSONField(default=dict)),
                ('ep_product_options', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'db_table': 'expert',
            },
        ),
    ]
