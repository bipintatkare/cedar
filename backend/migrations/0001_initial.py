# Generated by Django 4.0.4 on 2023-01-08 19:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import partial_date.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='adminModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='costCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='otpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('tim', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='reservationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservationNo', models.CharField(max_length=255)),
                ('guestFirstName', models.CharField(max_length=255)),
                ('guestLastName', models.CharField(max_length=255)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('room', models.CharField(max_length=255)),
                ('notes', models.TextField(blank=True, null=True)),
                ('unitNo', models.IntegerField()),
                ('subTotal', models.IntegerField()),
                ('revenue', models.FloatField()),
                ('currency', models.CharField(max_length=4)),
                ('adults', models.IntegerField(blank=True, null=True)),
                ('totalDays', models.IntegerField(default=1)),
                ('children', models.IntegerField(blank=True, null=True)),
                ('checkInDate', models.DateField(default=django.utils.timezone.now)),
                ('checkOutDate', models.DateField(default=django.utils.timezone.now)),
                ('createDate', models.DateField(default=django.utils.timezone.now)),
                ('klevioKey', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='sessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('tim', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='settingsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('calendar', models.TextField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('map', models.ImageField(blank=True, null=True, upload_to='map/')),
            ],
        ),
        migrations.CreateModel(
            name='expenseTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expense_category', to='backend.costcategorymodel')),
            ],
        ),
        migrations.CreateModel(
            name='costModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', partial_date.fields.PartialDateField()),
                ('amount', models.FloatField()),
                ('reciept', models.ImageField(blank=True, null=True, upload_to='reciept/')),
                ('expense', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cost_expense', to='backend.expensetypemodel')),
            ],
        ),
        migrations.CreateModel(
            name='costExpenseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', partial_date.fields.PartialDateField()),
                ('amount', models.FloatField()),
                ('reciept', models.ImageField(blank=True, null=True, upload_to='reciept/')),
                ('expense', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='costexpense_expense', to='backend.expensetypemodel')),
            ],
        ),
    ]
