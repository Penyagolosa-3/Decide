# Generated by Django 2.0 on 2021-12-19 17:30

from django.db import migrations, models
import voting.validators


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='voting',
            name='desc',
            field=models.TextField(blank=True, null=True, validators=[voting.validators.lofensivo]),
        ),
    ]