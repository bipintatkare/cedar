from django.db import models
from django.utils import timezone
#
from partial_date import PartialDateField
# Create your models here.


class settingsModel(models.Model):
    url = models.CharField(max_length=255)
    calendar = models.TextField()
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    map = models.ImageField(upload_to='map/', blank=True, null=True)


class sessionModel(models.Model):
    token = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    tim = models.DateTimeField(default=timezone.now)


class otpModel(models.Model):
    otp = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    tim = models.DateTimeField(default=timezone.now)


class adminModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    password = models.CharField(max_length=255)


class reservationModel(models.Model):
    reservationNo = models.CharField(max_length=255)
    guestFirstName = models.CharField(max_length=255)
    guestLastName = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    unitNo = models.IntegerField()
    subTotal = models.IntegerField()
    revenue = models.FloatField()
    currency = models.CharField(max_length=4)
    adults = models.IntegerField(blank=True, null=True)
    totalDays = models.IntegerField(default=1)
    children = models.IntegerField(blank=True, null=True)
    checkInDate = models.DateField(default=timezone.now)
    checkOutDate = models.DateField(default=timezone.now)
    createDate = models.DateField(default=timezone.now)
    klevioKey = models.BooleanField(default=False)


class costCategoryModel(models.Model):
    category = models.CharField(max_length=255)


class expenseTypeModel(models.Model):
    typ = models.CharField(max_length=255)
    category = models.ForeignKey(
        "costCategoryModel",
        related_name="expense_category",
        on_delete=models.CASCADE, blank=True, null=True
    )


class costModel(models.Model):
    # date = models.DateTimeField(default=timezone.now)
    date = PartialDateField()
    expense = models.ForeignKey(
        "expenseTypeModel",
        related_name="cost_expense",
        on_delete=models.CASCADE, blank=True, null=True
    )
    amount = models.FloatField()
    reciept = models.ImageField(upload_to='reciept/', blank=True, null=True)


class costExpenseModel(models.Model):
    # date = models.DateTimeField(default=timezone.now)
    date = PartialDateField()
    expense = models.ForeignKey(
        "expenseTypeModel",
        related_name="costexpense_expense",
        on_delete=models.CASCADE, blank=True, null=True
    )
    amount = models.FloatField()
    reciept = models.ImageField(upload_to='reciept/', blank=True, null=True)
