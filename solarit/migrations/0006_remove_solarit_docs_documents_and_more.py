# Generated by Django 4.2.2 on 2023-10-08 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solarit', '0005_remove_solarit_docs_prompt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solarit_docs',
            name='documents',
        ),
        migrations.AddField(
            model_name='solarit_docs',
            name='txt_documents',
            field=models.FileField(default=False, upload_to='uploaded_documents/txt_documents/'),
        ),
    ]