import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse

from Library.models import TempMembership, NotificationDB, ContactDB
from LibraryAdmin.models import LibraryMembersDB, LibraryBooksDB, BookCategoryDB, ReviewDB, Booking, BookRecords

# api views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BookSerializer, ReviewSerializer


@api_view(['GET'])
def get_books(request):
    books = LibraryBooksDB.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def bookdetail(req, id):
    details = LibraryBooksDB.objects.get(id=id)
    review = ReviewDB.objects.filter(bookname=details)
    serializer = BookSerializer(details)
    reviews_serializer = ReviewSerializer(review, many=True)
    return Response({
        'book': serializer.data,
        'review': reviews_serializer.data
    })


# Create your views here.
def Home(req):
    cat = BookCategoryDB.objects.all()
    data = LibraryBooksDB.objects.all()
    return render(req, "home.html", {'cat': cat, 'data': data})


def MemberLogin(req):
    return render(req, "login.html")


def MemberSignup(req):
    return render(req, "signup.html")


def Signup(req):
    if req.method == "POST":
        username = req.POST.get('name')
        password = req.POST.get('password')
        email = req.POST.get('email')
        phone = req.POST.get('phone')
        dob = req.POST.get('dob')
        obj = TempMembership(username=username, password=password, email=email, phone=phone, dob=dob)
        if LibraryMembersDB.objects.filter(username=username).exists():
            messages.warning(req, "User already exists..!")
            return redirect(MemberSignup)
        elif LibraryMembersDB.objects.filter(email=email).exists():
            messages.warning(req, "Email already in exists..!")
            return redirect(MemberSignup)
        else:
            obj.save()
            messages.warning(req, "You will get confirmation on your email once membership is activated ")
        return redirect(MemberLogin)


def Login(req):
    if req.method == "POST":
        username = req.POST.get('name')
        password = req.POST.get('password')
        if LibraryMembersDB.objects.filter(username=username, password=password).exists():
            member = LibraryMembersDB.objects.get(username=username, password=password)
            req.session['username'] = username
            req.session['password'] = password
            req.session['email'] = member.email
            messages.success(req, "login succesfull")
            return redirect('Home')
        else:
            messages.warning(req, "invalid Username or Password")
            return redirect('MemberLogin')
    else:
        messages.warning(req, "User not found..!")
        return redirect('MemberLogin')


def logout(req):
    del req.session['username']
    del req.session['password']
    del req.session['email']

    return redirect(Home)


def ShopPage(req):
    bookdata = LibraryBooksDB.objects.all()
    cat = BookCategoryDB.objects.all()
    paginator = Paginator(bookdata, 9)  # Show 6 books per page

    page = req.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)
    nbooks = 0
    for i in bookdata:
        nbooks = nbooks + 1

    return render(req, "shop.html", {'bookdata': bookdata, 'cat': cat, 'nbooks': nbooks, 'books': books})


def CategoryPage(req, gn):
    cat = BookCategoryDB.objects.all()
    bookdata = LibraryBooksDB.objects.all()
    data = LibraryBooksDB.objects.filter(genre=gn)
    paginator = Paginator(data, 9)  # Show 6 books per page

    page = req.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)
    nbooks = 0
    for i in data:
        nbooks = nbooks + 1
    return render(req, "category.html",
                  {'data': data, 'cat': cat, 'nbooks': nbooks, 'books': books, 'bookdata': bookdata})


def SearchCategory(req):
    cat = BookCategoryDB.objects.all()
    bookdata = LibraryBooksDB.objects.all()
    if req.method == "POST":
        key = req.POST.get('searchkey')
        data = (LibraryBooksDB.objects.filter(bname__icontains=key) | LibraryBooksDB.objects.filter(
            author__icontains=key) | LibraryBooksDB.objects.filter(genre__icontains=key)
                | LibraryBooksDB.objects.filter(genre__icontains=key))
        paginator = Paginator(data, 9)  # Show 6 books per page

        page = req.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            books = paginator.page(paginator.num_pages)
        nbooks = 0
        for i in data:
            nbooks = nbooks + 1
        return render(req, "category.html",
                      {'data': data, 'cat': cat, 'nbooks': nbooks, 'books': books, 'bookdata': bookdata})


import datetime
from django.shortcuts import render


def SingleBook(req, Id):
    cat = BookCategoryDB.objects.all()
    book = LibraryBooksDB.objects.get(id=Id)
    available = not Booking.objects.filter(book=book).exists()
    data = LibraryBooksDB.objects.all()
    date = (datetime.datetime.now().date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    avg_review = 0
    count = 0
    sum_reviews = 0

    if ReviewDB.objects.filter(bookname=book).exists():
        review = ReviewDB.objects.filter(bookname=book)
        for i in review:
            if i.review is not None:
                sum_reviews += i.review
                count += 1

        if count > 0:
            avg_review = sum_reviews / count
        if 'email' in req.session:
            user = req.session['email']
            user_details = LibraryMembersDB.objects.get(email=user)
            existing_review = ReviewDB.objects.filter(user=user_details, bookname=book).exists()

            if existing_review:
                exist_review = ReviewDB.objects.filter(user=user_details, bookname=book).first()
                return render(req, "single_book.html", {
                    'book': book,
                    'data': data,
                    'review': review,
                    'cat': cat,
                    'avg_review': avg_review,
                    "count": count,
                    "date": date,
                    "available": available,
                    'exist_review': exist_review
                })

        return render(req, "single_book.html", {
            'book': book,
            'data': data,
            'review': review,
            'cat': cat,
            'avg_review': avg_review,
            "count": count,
            "date": date,
            "available": available,
        })

    return render(req, "single_book.html", {
        'book': book,
        'data': data,
        'cat': cat,
        "date": date,
        "available": available
    })


def Review(req, Id):
    if 'email' not in req.session:
        messages.error(req, "You need to be logged in to leave a review.")
        return redirect(reverse('SingleBook', args=[Id]))
    else:
        user = req.session['email']
        user_details = LibraryMembersDB.objects.get(email=user)
        book = LibraryBooksDB.objects.get(id=Id)
        if req.method == "POST":
            review = req.POST.get('rating-1')
            comments = req.POST.get('message')
            if review is not None:
                obj = ReviewDB(user=user_details, bookname=book, review=review, comment=comments)
                obj.save()
                messages.success(req, "Review submitted successfully.")
            else:
                messages.error(req, "Select a rating..!")

            return redirect(reverse('SingleBook', args=[Id]))


def updateReview(req, Id, bid):
    if req.method == "POST":
        review = req.POST.get('rating-1')
        comments = req.POST.get('message')
        obj = ReviewDB.objects.filter(id=Id).update(review=review, comment=comments)
        return redirect(reverse('SingleBook', args=[bid]))


def ReserveBook(req):
    if 'username' in req.session:
        if req.method == "POST":
            bdate = req.POST.get('sdate')
            rdate = req.POST.get('rdate')
            email = req.POST.get('email')
            bid = req.POST.get('bid')
            user = LibraryMembersDB.objects.get(email=email)
            book = LibraryBooksDB.objects.get(id=bid)
            obj = Booking(user=user, book=book, booking_date=bdate, return_date=rdate)
            obj.save()
            messages.success(req, "Book Reserved Successfully")
            return redirect(reverse('SingleBook', args=[bid]))
    else:
        messages.error(req, "You need to be logged in to reserve a book")
        return redirect('MemberLogin')


def BorrowRecords(req):
    if 'username' in req.session:
        cat = BookCategoryDB.objects.all()
        username = req.session['username']
        user = LibraryMembersDB.objects.get(username=username)
        pending_books = BookRecords.objects.filter(user=user, status='pending')
        due_books = BookRecords.objects.filter(user=user, status='Due')
        returned_books = BookRecords.objects.filter(user=user, status='Returned')
        records = list(due_books) + list(pending_books) + list(returned_books)
        return render(req, "bookrecords.html", {'records': records, 'cat': cat})
    else:
        messages.error(req, "Login Required")
        return redirect(Home)


def ContactPage(req):
    cat = BookCategoryDB.objects.all()
    return render(req, "contact.html", {'cat': cat})


def SaveContact(req):
    if req.method == "POST":
        name = req.POST.get('name')
        email = req.POST.get('email')
        subject = req.POST.get('subject')
        message = req.POST.get('message')
        obj = ContactDB(name=name, email=email, subject=subject, message=message)
        obj.save()
        msg = """
        Dear Customer,

        Thank you for reaching out to us through our contact page. We have received your message and will get back to you as soon as possible. Your inquiry is important to us, and we aim to provide a timely response.

        If you need immediate assistance, please feel free to call us at (91) 9207287491.

        Thank you for your patience.

        Best regards,  
        Admin  
        Library  
        Kochi, Kerala.
        Kakanadu, 682303 
        library@gmail.com
        """
        sub = "Thank You for Your Response"
        send_mail(sub, msg, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        messages.success(req, "Message sent successfully")
        return redirect(Home)


def Notification(req, uname):
    cat = BookCategoryDB.objects.all()
    user = LibraryMembersDB.objects.get(username=uname)
    notice = NotificationDB.objects.filter(user=user).order_by('-id')
    return render(req, "mails.html", {'notice': notice, 'cat': cat})


def deleteNotification(req, ID):
    data = NotificationDB.objects.filter(id=ID)
    uname = req.session['username']
    data.delete()
    return redirect(Notification, uname)


def AboutPage(req):
    cat = BookCategoryDB.objects.all()
    return render(req, "about.html", {'cat': cat})
