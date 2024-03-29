# Generated by Django 4.1.7 on 2023-03-16 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('due_data', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'К выполнению'), (2, 'В процессе'), (3, 'Выполнено'), (4, 'Архив')], default=1)),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий'), (4, 'Очень высокий')], default=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goals', to='goals.goalcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Цель',
                'verbose_name_plural': 'Цели',
            },
        ),
    ]
