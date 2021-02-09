# Generated by Django 3.1.5 on 2021-02-05 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products_app', '0005_auto_20210204_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=30, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='published',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50, verbose_name='Автор')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('published', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products_app.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-published'],
            },
        ),
    ]
