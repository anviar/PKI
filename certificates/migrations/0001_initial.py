# Generated by Django 2.0.6 on 2018-08-28 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('private_key', models.TextField(blank=True, null=True)),
                ('conf', models.TextField(blank=True, null=True)),
                ('csr', models.TextField(blank=True, null=True)),
                ('crt', models.TextField(blank=True, null=True)),
                ('intermediate', models.TextField(blank=True, null=True)),
                ('valid', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('domain_name', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='certificate',
            name='domain_name',
            field=models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='certificates.Domain'),
        ),
    ]