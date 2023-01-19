# Generated by Django 4.0.2 on 2022-09-10 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0002_remove_curriculum_course_level_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('role', models.CharField(choices=[('ICT1', 'ICT1'), ('ICT2', 'ICT2'), ('ICT3', 'ICT3'), ('FO', 'Faculty Officer'), ('EO', 'Exam officer'), ('LA', 'Level Adviser'), ('LEC', 'Lecturer')], max_length=50)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('programme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='base.programme')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.staff', to_field='userid')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='LevelAdviser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=10)),
                ('approved_at', models.DateTimeField(auto_now_add=True)),
                ('approval_details', models.TextField(blank=True, null=True)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='users', to=settings.AUTH_USER_MODEL)),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.programme')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.setting')),
            ],
            options={
                'db_table': 'lecturer_level_adviser',
            },
        ),
    ]
