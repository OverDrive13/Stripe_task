# Generated by Django 4.2.15 on 2024-08-29 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-id'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-id'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='order',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tax',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('rub', 'RUB'), ('usd', 'USD')], default='rub', max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='api.item', verbose_name='Товары'),
        ),
        migrations.DeleteModel(
            name='Discount',
        ),
        migrations.DeleteModel(
            name='Tax',
        ),
    ]
