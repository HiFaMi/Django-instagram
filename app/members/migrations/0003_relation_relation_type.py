# Generated by Django 2.0.6 on 2018-06-29 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_remove_relation_relation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='relation_type',
            field=models.CharField(choices=[('f', 'Follow'), ('b', 'Block')], default='f', max_length=1),
            preserve_default=False,
        ),
    ]