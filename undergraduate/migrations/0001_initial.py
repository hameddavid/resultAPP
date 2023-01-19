# Generated by Django 4.1.3 on 2022-12-15 08:16

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
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=50)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ug_departments',
            },
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=30, null=True)),
                ('surname', models.CharField(blank=True, max_length=30, null=True)),
                ('Lecturer_id', models.CharField(blank=True, max_length=30, null=True)),
                ('programme', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('campus_text', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_date', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.CharField(default='N', max_length=1)),
                ('login_name', models.CharField(blank=True, max_length=30, null=True)),
                ('courses', models.TextField(blank=True, null=True)),
                ('prog_code', models.TextField(blank=True, null=True)),
                ('user_code', models.CharField(blank=True, max_length=191, null=True)),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('notify_sms', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'ug_lecturer',
            },
        ),
        migrations.CreateModel(
            name='OutstandException',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(blank=True, max_length=30, null=True)),
                ('course_code', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_date', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.CharField(blank=True, max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ug_outstanding_exception',
            },
        ),
        migrations.CreateModel(
            name='RunregTransHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.IntegerField()),
                ('matric_number', models.CharField(max_length=100)),
                ('course_code', models.CharField(blank=True, max_length=30, null=True)),
                ('action_message', models.TextField(blank=True, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_date', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ug_Runreg_trans_history',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=10)),
                ('semester', models.CharField(max_length=15)),
                ('session_desc', models.CharField(max_length=100)),
                ('start_date', models.CharField(blank=True, max_length=30, null=True)),
                ('end_date', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_by', models.CharField(blank=True, max_length=50, null=True)),
                ('last_updated_date', models.CharField(blank=True, max_length=50, null=True)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(max_length=50, unique=True)),
                ('surname', models.CharField(blank=True, max_length=50, null=True)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('sex', models.CharField(blank=True, max_length=1, null=True)),
                ('birth_date', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('lga', models.CharField(blank=True, max_length=191, null=True)),
                ('current_level', models.CharField(blank=True, max_length=5, null=True)),
                ('state_origin', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('programme', models.CharField(blank=True, max_length=191, null=True)),
                ('city_resident', models.CharField(blank=True, max_length=100, null=True)),
                ('state_resident', models.CharField(blank=True, max_length=100, null=True)),
                ('matric_date', models.CharField(blank=True, max_length=50, null=True)),
                ('graduation_date', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('last_updated_by_old', models.CharField(blank=True, default=' ', max_length=50, null=True)),
                ('last_update_date_old', models.CharField(blank=True, max_length=50, null=True)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('ctcp', models.IntegerField(blank=True, null=True)),
                ('ctnur', models.IntegerField(blank=True, null=True)),
                ('ctnup', models.IntegerField(blank=True, null=True)),
                ('ctnuf', models.IntegerField(blank=True, null=True)),
                ('cgpa', models.FloatField(blank=True, null=True)),
                ('email1', models.CharField(blank=True, max_length=100, null=True)),
                ('email2', models.CharField(blank=True, max_length=100, null=True)),
                ('student_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('parent_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('prog_code', models.CharField(blank=True, max_length=50, null=True)),
                ('picture', models.CharField(blank=True, max_length=191, null=True)),
                ('ctcup', models.IntegerField(blank=True, null=True)),
                ('cteup', models.IntegerField(blank=True, null=True)),
                ('notify_sms', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('notify_email', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('parent_pwd', models.CharField(blank=True, max_length=191, null=True)),
                ('registration_pwd', models.CharField(blank=True, default='password', max_length=191, null=True)),
                ('financial_flag', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('notify_bursary_sms', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('jamb_reg', models.CharField(blank=True, max_length=50, null=True)),
                ('run_mail', models.CharField(blank=True, max_length=100, null=True)),
                ('degree_sought', models.CharField(blank=True, max_length=100, null=True)),
                ('acad_status', models.CharField(blank=True, default='GSD', max_length=50, null=True)),
                ('entry_mode', models.CharField(blank=True, default='UME', max_length=50, null=True)),
                ('hold_record', models.CharField(blank=True, max_length=1, null=True)),
                ('run_mail_2', models.CharField(blank=True, max_length=191, null=True)),
                ('gpa', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by_new', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_student_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_students',
            },
        ),
        migrations.CreateModel(
            name='RegSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(blank=True, max_length=30, null=True)),
                ('semester', models.CharField(blank=True, max_length=30, null=True)),
                ('session_id', models.CharField(blank=True, max_length=30, null=True)),
                ('courses_taken', models.IntegerField(blank=True, null=True)),
                ('courses_passed', models.IntegerField(blank=True, null=True)),
                ('courses_failed', models.IntegerField(blank=True, null=True)),
                ('tnur', models.IntegerField(blank=True, null=True)),
                ('tnup', models.IntegerField(blank=True, null=True)),
                ('tnuf', models.IntegerField(blank=True, null=True)),
                ('wcrp', models.IntegerField(blank=True, null=True)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=5)),
                ('remarks', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_by_old', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_date_old', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.CharField(blank=True, max_length=1, null=True)),
                ('ctnur', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ctnup', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ctcp', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ctcup', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('cteup', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('acad_status', models.CharField(blank=True, max_length=30, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by_new', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_reg_summary_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_reg_summary',
            },
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('programme_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('programme', models.CharField(max_length=50)),
                ('required_ctcup', models.IntegerField(default=0)),
                ('required_cteup', models.IntegerField(default=0)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='undergraduate.department')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_programme_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_programmes',
            },
        ),
        migrations.CreateModel(
            name='History1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.IntegerField()),
                ('matric_number', models.CharField(blank=True, max_length=30, null=True)),
                ('course_code', models.CharField(blank=True, max_length=30, null=True)),
                ('action_message', models.TextField(blank=True, null=True)),
                ('deleted', models.CharField(blank=True, max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_history1_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_history1',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.CharField(max_length=191)),
                ('last_updated_by_old', models.CharField(default=' ', max_length=191)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by_new', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='ug_faculty_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_faculties',
            },
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(blank=True, max_length=30, null=True)),
                ('message_date', models.CharField(blank=True, max_length=30, null=True)),
                ('message_desc', models.TextField(blank=True, null=True)),
                ('last_updated_date', models.CharField(blank=True, max_length=25, null=True)),
                ('deleted', models.CharField(blank=True, max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_errorlog_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_errorLog',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='undergraduate.faculty'),
        ),
        migrations.AddField(
            model_name='department',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_department_user_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=45)),
                ('course_title', models.CharField(blank=True, max_length=191, null=True)),
                ('unit', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('course_id_of_equivalence', models.CharField(blank=True, max_length=45, null=True)),
                ('last_updated_by_old', models.CharField(blank=True, max_length=45, null=True)),
                ('last_update_date', models.CharField(blank=True, max_length=45, null=True)),
                ('course_level', models.CharField(blank=True, max_length=10, null=True)),
                ('register_flag', models.CharField(blank=True, max_length=10, null=True)),
                ('deleted', models.CharField(blank=True, max_length=1, null=True)),
                ('unit_id', models.CharField(blank=True, max_length=45, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by_new', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_course_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_courses',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_number', models.CharField(max_length=30)),
                ('semester', models.CharField(max_length=30)),
                ('session_id', models.CharField(max_length=30)),
                ('course_code', models.CharField(max_length=30)),
                ('Lecturer_id', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(max_length=5)),
                ('score', models.IntegerField()),
                ('grade', models.CharField(blank=True, max_length=5, null=True)),
                ('remarks', models.CharField(blank=True, max_length=45, null=True)),
                ('last_updated_date_old', models.CharField(blank=True, max_length=30, null=True)),
                ('last_updated_by_old', models.CharField(blank=True, max_length=30, null=True)),
                ('deleted', models.CharField(blank=True, default='N', max_length=1, null=True)),
                ('satisfied', models.CharField(blank=True, max_length=5, null=True)),
                ('unit_id', models.CharField(max_length=10)),
                ('app_user_id', models.CharField(blank=True, max_length=191, null=True)),
                ('level', models.CharField(blank=True, max_length=5, null=True)),
                ('record_status', models.CharField(blank=True, default='OFF', max_length=5, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by_new', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_registration_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_registration',
                'unique_together': {('matric_number', 'semester', 'session_id', 'course_code')},
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(max_length=10)),
                ('course_code', models.CharField(max_length=15)),
                ('status', models.CharField(choices=[('E', 'ELECTTIVE'), ('C', 'COMPULSORY')], default='C', max_length=1)),
                ('last_updated_by_old', models.CharField(blank=True, default=' ', max_length=191, null=True)),
                ('last_updated_date_old', models.CharField(blank=True, max_length=191, null=True)),
                ('course_reg_level', models.CharField(choices=[('100', '100'), ('200', '200'), ('300', '300'), ('400', '400'), ('500', '500'), ('600', '600'), ('700', '700')], default='100', max_length=10)),
                ('semester', models.CharField(max_length=1)),
                ('register_flag', models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], default='Y', max_length=2)),
                ('deleted', models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], default='N', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_updated_by_new', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_curriculum_user_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ug_curriculum',
                'unique_together': {('program', 'course_code')},
            },
        ),
    ]
