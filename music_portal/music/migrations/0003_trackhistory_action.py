# Generated by Django 5.1.4 on 2024-12-05 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_trackhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackhistory',
            name='action',
            field=models.CharField(default='played', max_length=50),
        ),
    ]
