# Generated by Django 2.2 on 2019-05-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('response', '0004_auto_20190506_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱'),
        ),
    ]