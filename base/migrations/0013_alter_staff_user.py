# Generated by Django 4.1.3 on 2023-03-20 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_product_name_alter_product_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]