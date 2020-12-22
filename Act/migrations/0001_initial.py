# Generated by Django 2.2.7 on 2020-12-22 09:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='name', max_length=150)),
                ('isActive', models.BooleanField(db_column='isActive', default=True)),
                ('period', models.DateTimeField(blank=True, db_column='period', db_index=True, default=datetime.datetime.now)),
                ('comment', models.TextField(blank=True, db_column='comment')),
            ],
            options={
                'verbose_name': 'Этап',
                'verbose_name_plural': 'Список этапов задач',
                'db_table': 'Act',
                'ordering': ['parent', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='name', max_length=150)),
                ('comment', models.TextField(blank=True, db_column='comment')),
                ('isActive', models.BooleanField(db_column='isActive', default=True)),
                ('begin', models.DateTimeField(auto_now_add=True, db_column='begin', db_index=True)),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Список задач',
                'db_table': 'Notification',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NotificationState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='name', max_length=30, unique=True)),
                ('isActive', models.BooleanField(db_column='isActive', default=True)),
                ('red', models.IntegerField(db_column='red', default=0)),
                ('green', models.IntegerField(db_column='green', default=0)),
                ('blue', models.IntegerField(db_column='blue', default=0)),
                ('background_red', models.IntegerField(db_column='background_red', default=255)),
                ('background_green', models.IntegerField(db_column='background_green', default=255)),
                ('background_blue', models.IntegerField(db_column='background_blue', default=255)),
            ],
            options={
                'verbose_name': 'Состояние',
                'verbose_name_plural': 'Состояния задач',
                'db_table': 'NotificationState',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SubActComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateTimeField(blank=True, db_column='period', db_index=True, default=datetime.datetime.now)),
                ('comment', models.TextField(blank=True, db_column='comment')),
                ('act', models.ForeignKey(blank=True, db_column='act', null=True, on_delete=django.db.models.deletion.CASCADE, to='Act.Act')),
            ],
            options={
                'verbose_name': 'Комментарий к этапу',
                'verbose_name_plural': 'Комментарии этапов',
                'db_table': 'SubActComments',
                'ordering': ['-period'],
            },
        ),
        migrations.CreateModel(
            name='HistorySubActComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, db_column='comment')),
                ('period', models.DateTimeField(blank=True, db_column='period', db_index=True, default=datetime.datetime.now)),
                ('actComment', models.ForeignKey(blank=True, db_column='actComment', null=True, on_delete=django.db.models.deletion.CASCADE, to='Act.SubActComments')),
            ],
            options={
                'verbose_name': 'История изменений комментия этапа',
                'verbose_name_plural': 'Истории изменений комментариев этапов',
                'db_table': 'HistorySubActComments',
                'ordering': ['-period'],
            },
        ),
        migrations.AddField(
            model_name='act',
            name='parent',
            field=models.ForeignKey(blank=True, db_column='parent', null=True, on_delete=django.db.models.deletion.CASCADE, to='Act.Notification'),
        ),
        migrations.AddField(
            model_name='act',
            name='state',
            field=models.ForeignKey(blank=True, db_column='state', default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='Act.NotificationState'),
        ),
        migrations.CreateModel(
            name='ActHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateTimeField(blank=True, db_column='period', db_index=True, default=datetime.datetime.now)),
                ('act', models.ForeignKey(blank=True, db_column='act', null=True, on_delete=django.db.models.deletion.CASCADE, to='Act.Act')),
                ('state', models.ForeignKey(blank=True, db_column='state', null=True, on_delete=django.db.models.deletion.PROTECT, to='Act.NotificationState')),
            ],
            options={
                'verbose_name': 'История состояния',
                'verbose_name_plural': 'Истории изменения состояний',
                'db_table': 'NotificationHistory',
                'ordering': ['-act', '-period'],
                'unique_together': {('period', 'act')},
            },
        ),
    ]
