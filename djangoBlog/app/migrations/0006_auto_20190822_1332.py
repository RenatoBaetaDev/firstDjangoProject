# Generated by Django 2.2.4 on 2019-08-22 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190822_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(blank=True, max_length=64, upload_to='documents/'),
        ),
    ]