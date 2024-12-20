# Generated by Django 5.1.4 on 2024-12-21 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deity_rating', models.IntegerField()),
                ('tilak_rating', models.IntegerField()),
                ('leela_rating', models.IntegerField()),
                ('samatha_rating', models.IntegerField()),
                ('deposit_rating', models.IntegerField()),
                ('water_rating', models.IntegerField()),
                ('wash_rating', models.IntegerField()),
                ('accessibility_rating', models.IntegerField()),
                ('parking_rating', models.IntegerField()),
                ('food_rating', models.IntegerField()),
                ('shopping_rating', models.IntegerField()),
                ('kids_rating', models.IntegerField()),
                ('entry_rating', models.IntegerField()),
                ('directions_rating', models.IntegerField()),
                ('overall_rating', models.IntegerField()),
                ('feedback', models.IntegerField(blank=True)),
                ('contact', models.IntegerField(blank=True)),
            ],
        ),
    ]
