from django.db import models

from LibraryAdmin.models import LibraryMembersDB, BookRecords, LibraryBooksDB


# Create your models here.


class TempMembership(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)


class NotificationDB(models.Model):
    user = models.ForeignKey(LibraryMembersDB, on_delete=models.CASCADE)
    records = models.ForeignKey(BookRecords, on_delete=models.CASCADE)
    sub = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)


class ContactDB(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=50, null=True, blank=True)



