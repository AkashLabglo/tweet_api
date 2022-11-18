# Generated by Django 4.1.2 on 2022-11-18 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_account', '0002_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('tweet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tweet_account.tweet')),
            ],
            options={
                'abstract': False,
            },
            bases=('tweet_account.tweet',),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('reference_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tweet_account.reference')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweet_account.tweet')),
            ],
            options={
                'abstract': False,
            },
            bases=('tweet_account.reference',),
        ),
    ]