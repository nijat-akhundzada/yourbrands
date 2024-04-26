# Generated by Django 5.0.3 on 2024-04-26 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_parentcategory_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentcategory',
            name='gender',
            field=models.ManyToManyField(related_name='parent_categories', to='api.gender'),
        ),
        migrations.AlterField(
            model_name='parentcategory',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
