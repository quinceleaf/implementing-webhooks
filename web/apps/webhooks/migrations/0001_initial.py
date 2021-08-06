# Generated by Django 3.2.6 on 2021-08-06 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebhookMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(help_text='When event was received')),
                ('payload', models.JSONField(default=None, null=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='webhookmessage',
            index=models.Index(fields=['received_at'], name='webhooks_we_receive_291393_idx'),
        ),
    ]
