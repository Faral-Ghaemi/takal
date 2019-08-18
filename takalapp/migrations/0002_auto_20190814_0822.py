# Generated by Django 2.1.5 on 2019-08-14 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('takalapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=1, verbose_name='تعداد')),
                ('date', models.DateField(auto_now_add=True, verbose_name='تاریخ')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام')),
                ('score', models.CharField(max_length=200, verbose_name='امتیاز مورد نیاز')),
                ('image', models.ImageField(upload_to='images/', verbose_name='تصویر محصول')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('owner', models.CharField(max_length=200)),
                ('store_lat', models.CharField(max_length=200)),
                ('store_lng', models.CharField(max_length=200)),
                ('score', models.IntegerField()),
                ('phone', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('startpoint_lat', models.CharField(max_length=200)),
                ('startpoint_lng', models.CharField(max_length=200)),
                ('passeddistance', models.CharField(blank=True, max_length=200, null=True)),
                ('burenedcalory', models.CharField(blank=True, max_length=200, null=True)),
                ('avgspeed', models.CharField(blank=True, max_length=200, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('endpoint_lat', models.CharField(blank=True, max_length=200, null=True)),
                ('endpoint_lng', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='score',
            field=models.CharField(default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.CharField(max_length=246, unique=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='takalapp.Profile'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='takalapp.Store'),
        ),
        migrations.AddField(
            model_name='offer',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='takalapp.Product', verbose_name='محصول'),
        ),
        migrations.AddField(
            model_name='offer',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='takalapp.Profile', verbose_name='نام کاربری'),
        ),
        migrations.AddField(
            model_name='offer',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='takalapp.Store', verbose_name='فروشگاه'),
        ),
    ]