# Generated by Django 2.1.4 on 2018-12-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=250, unique=True)),
                ('value', models.TextField()),
                ('label', models.CharField(max_length=500)),
            ],
        ),
    ]
