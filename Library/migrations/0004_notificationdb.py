# Generated by Django 5.0.6 on 2024-07-28 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0003_delete_reviewdb'),
        ('LibraryAdmin', '0008_sentemail'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.CharField(blank=True, max_length=100, null=True)),
                ('records', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LibraryAdmin.bookrecords')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LibraryAdmin.librarymembersdb')),
            ],
        ),
    ]
