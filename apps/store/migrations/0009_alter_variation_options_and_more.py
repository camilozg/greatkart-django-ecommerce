# Generated by Django 4.1.6 on 2023-02-20 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_variation_category_variation_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variation',
            options={'verbose_name': 'varciación', 'verbose_name_plural': 'variaciones'},
        ),
        migrations.AlterUniqueTogether(
            name='variation',
            unique_together={('product', 'category', 'value')},
        ),
    ]