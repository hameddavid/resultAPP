# Generated by Django 4.1.3 on 2023-01-11 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0004_lecturercourse'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='registration',
            name='matric_number_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_reg_stud_related', to='undergraduate.student', to_field='matric_number'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='deleted',
            field=models.CharField(choices=[('N', 'N'), ('Y', 'Y')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='registration',
            name='unit_id',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('course_code', 'unit_id')},
        ),
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together={('matric_number_fk', 'semester', 'session_id', 'course_code')},
        ),
        migrations.RemoveField(
            model_name='registration',
            name='matric_number',
        ),
    ]