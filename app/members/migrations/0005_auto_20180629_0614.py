# Generated by Django 2.0.6 on 2018-06-29 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20180629_0538'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together={('from_user', 'to_user')},
        ),
    ]