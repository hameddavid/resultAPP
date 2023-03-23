# Generated by Django 4.1.3 on 2023-03-21 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0040_alter_curriculum_programme_and_more'),
        ('users', '0042_alter_loguserroleforsemester_programme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leveladviser',
            name='programme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='undergraduate.programme', to_field='programme_code'),
        ),
        migrations.AlterField(
            model_name='loguserroleforsemester',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='programme_semester_role_related', to='undergraduate.programme', to_field='programme_code'),
        ),
    ]
