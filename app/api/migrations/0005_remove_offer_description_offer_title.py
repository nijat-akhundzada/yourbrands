# Generated by Django 5.0.3 on 2024-04-26 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_product_color_alter_product_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='description',
        ),
        migrations.AddField(
            model_name='offer',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]