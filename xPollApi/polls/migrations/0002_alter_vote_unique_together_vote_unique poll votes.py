# Generated by Django 4.0.2 on 2022-03-10 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('poll', 'voted_by'), name='unique poll votes'),
        ),
    ]