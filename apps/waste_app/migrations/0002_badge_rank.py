# Generated by Django 3.0.8 on 2020-07-30 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
