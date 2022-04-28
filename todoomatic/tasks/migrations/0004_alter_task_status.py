# Generated by Django 3.2.13 on 2022-04-28 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_assigntask_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Done', 'Done'), ('Cancelled', 'Cancelled')], default='Pending', max_length=200),
        ),
    ]
