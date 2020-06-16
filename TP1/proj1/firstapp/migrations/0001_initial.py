# Generated by Django 2.2 on 2020-03-27 19:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(default=' ', primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(default=' ', max_length=50)),
                ('last_name', models.CharField(default=' ', max_length=50)),
                ('email', models.EmailField(default=' ', max_length=50)),
                ('address', models.CharField(default=' ', max_length=100)),
                ('phone', models.CharField(default=' ', max_length=30)),
                ('gender', models.CharField(default=' ', max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=500)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='firstapp.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(default='DR.', max_length=20)),
                ('edu', models.CharField(default='MBBS', max_length=20)),
                ('join_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('speciality', models.CharField(default=' ', max_length=50)),
                ('status', models.CharField(choices=[('AC', 'Active'), ('IC', 'Inactive')], default='AC', max_length=2)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='firstapp.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('status', models.CharField(choices=[('PD', 'Pending'), ('AP', 'Approved'), ('RJ', 'rejected')], default='PD', max_length=2)),
                ('message', models.CharField(default='Pending Approval', max_length=1000)),
                ('Doctor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.Patient')),
            ],
        ),
    ]
