# Generated by Django 2.1.8 on 2019-08-31 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='sale',
            field=models.IntegerField(default=0, verbose_name='销量'),
        ),
        migrations.AddField(
            model_name='goods',
            name='unite',
            field=models.CharField(default='500g', max_length=20, verbose_name='单位'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='number',
            field=models.IntegerField(default=0, verbose_name='库存'),
        ),
    ]