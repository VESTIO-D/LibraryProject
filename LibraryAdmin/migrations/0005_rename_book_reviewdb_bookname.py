# Generated by Django 5.0.6 on 2024-06-23 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryAdmin', '0004_rename_username_reviewdb_user_remove_reviewdb_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewdb',
            old_name='book',
            new_name='bookname',
        ),
    ]
