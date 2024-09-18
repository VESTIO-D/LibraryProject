from django.db import models


# Create your models here.
class BookCategoryDB(models.Model):
    genre = models.CharField(max_length=100, null=True, blank=True)
    ccode = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)


class LibraryBooksDB(models.Model):
    bname = models.CharField(max_length=100, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    b_img = models.ImageField(upload_to="BookImage", null=True, blank=True)


class LibraryMembersDB(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class ReviewDB(models.Model):
    user = models.ForeignKey(LibraryMembersDB, on_delete=models.CASCADE)
    bookname = models.ForeignKey(LibraryBooksDB, on_delete=models.CASCADE)
    review = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)


class Booking(models.Model):
    user = models.ForeignKey(LibraryMembersDB, on_delete=models.CASCADE)
    book = models.ForeignKey(LibraryBooksDB, on_delete=models.CASCADE)
    orderid = models.AutoField(primary_key=True)
    booking_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)


class BookRecords(models.Model):
    user = models.ForeignKey(LibraryMembersDB, on_delete=models.CASCADE)
    book = models.ForeignKey(LibraryBooksDB, on_delete=models.CASCADE)
    orderid = models.AutoField(primary_key=True)
    return_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    collected_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    notification = models.BooleanField(default=False)


class SentEmail(models.Model):
    user = models.ForeignKey(LibraryMembersDB, on_delete=models.CASCADE)
    book_record = models.ForeignKey(BookRecords, on_delete=models.CASCADE)
    email_sent_date = models.DateField(auto_now_add=True)