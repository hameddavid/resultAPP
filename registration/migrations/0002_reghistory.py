# Generated by Django 4.0.2 on 2022-03-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(default=0, max_length=50)),
                ('course_code', models.CharField(default=0, max_length=7)),
                ('action_message', models.TextField(blank=True, default=0, null=True)),
                ('last_updated_by', models.CharField(blank=True, default=0, max_length=191, null=True)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'RegHistory',
            },
        ),
    ]
