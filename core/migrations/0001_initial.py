# Generated by Django 4.1.6 on 2023-03-13 13:10

import core.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('date_enrolled', models.DateField(default=django.utils.timezone.now)),
                ('points', models.IntegerField(default=0, editable=False)),
                ('profits', models.IntegerField(default=0, editable=False)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('date_enrolled', models.DateField(default=django.utils.timezone.now)),
                ('available', models.BooleanField(default=True)),
                ('orders_count', models.IntegerField(default=0, editable=False)),
                ('category', models.CharField(choices=[('drink', 'Drink'), ('snack', 'Snack'), ('dessert', 'Dessert'), ('NA', 'NA')], max_length=20)),
                ('image', models.ImageField(upload_to=core.models.Item.get_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_issued', models.DateTimeField(default=datetime.datetime.now)),
                ('fullfilled', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_issued', models.DateTimeField()),
                ('QR', models.ImageField(upload_to='QRs/%Y/%m/%d')),
                ('people_count', models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4)], default=1, verbose_name='persons')),
                ('customer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(editable=False, max_length=20)),
                ('net', models.IntegerField(editable=False)),
                ('discount', models.IntegerField(blank=True, default=0)),
                ('order', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='core.order')),
            ],
        ),
    ]
