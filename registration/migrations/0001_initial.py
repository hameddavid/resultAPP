# Generated by Django 4.0.2 on 2022-03-29 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(max_length=50)),
                ('semester', models.CharField(max_length=1)),
                ('session', models.CharField(max_length=9)),
                ('course_code', models.CharField(max_length=7)),
                ('lecturer_id', models.CharField(blank=True, default=0, max_length=20, null=True)),
                ('status', models.CharField(default='C', max_length=1)),
                ('score', models.CharField(default=-1, max_length=2)),
                ('grade', models.CharField(blank=True, default=0, max_length=1, null=True)),
                ('remarks', models.CharField(blank=True, default=0, max_length=60, null=True)),
                ('last_updated_date', models.CharField(blank=True, max_length=191, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=191, null=True)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('satisfied', models.CharField(blank=True, default=0, max_length=1, null=True)),
                ('unit_id', models.CharField(default=0, max_length=8)),
            ],
            options={
                'db_table': 'registration',
                'unique_together': {('matric_number', 'semester', 'session', 'course_code')},
            },
        ),
    ]
