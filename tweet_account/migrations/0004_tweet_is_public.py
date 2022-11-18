# Generated by Django 4.1.2 on 2022-11-18 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_account', '0003_reference_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='is_public',
            field=models.BooleanField(choices=[(False, 'Public'), (True, 'Private')], default=False, help_text='0-Public, 1-Private'),
        ),
    ]