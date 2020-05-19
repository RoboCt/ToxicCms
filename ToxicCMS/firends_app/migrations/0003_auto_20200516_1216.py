# Generated by Django 2.2.3 on 2020-05-16 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_remove_profile_friends'),
        ('firends_app', '0002_auto_20200514_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendslist',
            name='user_one',
        ),
        migrations.RemoveField(
            model_name='friendslist',
            name='user_two',
        ),
        migrations.AddField(
            model_name='friendslist',
            name='friend',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='userprofile.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendslist',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='person', to='userprofile.Profile'),
            preserve_default=False,
        ),
    ]