# Generated by Django 2.1.3 on 2018-11-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_auto_20181124_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailaddress',
            name='type',
            field=models.CharField(choices=[('private', 'private'), ('work', 'work')], max_length=50),
        ),
    ]
