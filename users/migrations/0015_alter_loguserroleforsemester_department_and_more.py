# Generated by Django 4.1.3 on 2022-12-27 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_setting_semester_open_close'),
        ('undergraduate', '0002_alter_curriculum_program_alter_curriculum_semester'),
        ('users', '0014_remove_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loguserroleforsemester',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='department_semester_role_related', to='base.department'),
        ),
        migrations.AlterField(
            model_name='loguserroleforsemester',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='programme_semester_role_related', to='base.programme'),
        ),
        migrations.AlterField(
            model_name='loguserroleforsemester',
            name='role_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED')], default='PENDING', max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='undergraduate.department'),
        ),
        migrations.AlterField(
            model_name='user',
            name='programme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='undergraduate.programme'),
        ),
    ]