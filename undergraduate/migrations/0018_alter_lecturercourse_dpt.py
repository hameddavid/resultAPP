# Generated by Django 4.1.3 on 2023-02-16 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0017_lecturercourse_dpt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturercourse',
            name='dpt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='undergraduate.department'),
        ),
    ]
