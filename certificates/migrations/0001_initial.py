# Generated by Django 2.0.3 on 2018-03-23 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('domain_name', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('owner', models.CharField(blank=True, max_length=256, null=True)),
                ('private_key', models.CharField(blank=True, max_length=512, null=True)),
                ('conf', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
