# Generated by Django 4.2.2 on 2023-10-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solarit', '0008_template_alter_solarit_docs_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solarit_docs',
            name='txt_documents',
            field=models.FileField(blank=True, default=False, upload_to='txt_documents/'),
        ),
    ]
