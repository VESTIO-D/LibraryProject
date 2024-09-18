import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from Library.models import TempMembership, NotificationDB, ContactDB
from LibraryAdmin.models import BookCategoryDB, LibraryBooksDB, LibraryMembersDB, Booking, BookRecords, SentEmail
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings



# Create your views here
def home(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr+req_no
    context = {
        'alert':alert,
        'reqr':reqr,
        'req_no':req_no
    }
    return render(req, "index.html", context)


def genrepage(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
        'alert': alert,
        'reqr': reqr,
        'req_no': req_no
    }
    return render(req, "genre.html", context)


def genretable(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = BookCategoryDB.objects.all()
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
        'alert': alert,
        'reqr': reqr,
        'req_no': req_no,
        'data': data
    }

    return render(req, "genretable.html", context)


def AddGenre(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    if req.method == "POST":
        genre = req.POST.get('genre')
        description = req.POST.get('description')
        ccode = req.POST.get('ccode')
        obj = BookCategoryDB(genre=genre, ccode=ccode, description=description)
        obj.save()
        messages.success(req, "saved successfully...!")
        return redirect(genrepage)


def Gedit(req, GId):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = BookCategoryDB.objects.get(id=GId)
    return render(req, "Gedit.html", {'data': data})


def UpdateGenre(req, GId):
    if req.method == "POST":
        genre = req.POST.get('genre')
        description = req.POST.get('description')
        ccode = req.POST.get('ccode')
        BookCategoryDB.objects.filter(id=GId).update(genre=genre, description=description, ccode=ccode)
        messages.success(req, "updated successfully")
        return redirect(genretable)


def DeleteGenre(req, GId):
    data = BookCategoryDB.objects.filter(id=GId)
    data.delete()
    messages.error(req, "Deleted successfully")
    return redirect(genretable)


def bookpage(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = BookCategoryDB.objects.all()

    return render(req, "books.html", {'data': data})


def addbook(req):
    if req.method == "POST":
        bname = req.POST.get('bname')
        genre = req.POST.get('genre')
        auhtor = req.POST.get('author')
        price = req.POST.get('price')
        description = req.POST.get('description')
        b_img = req.FILES['b_img']
        obj = LibraryBooksDB(bname=bname, genre=genre, price=price, description=description, b_img=b_img, author=auhtor)
        obj.save()
        messages.success(req, "saved successfully...!")
        return redirect(bookpage)


def booktable(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = LibraryBooksDB.objects.all()
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
        'alert': alert,
        'reqr': reqr,
        'req_no': req_no,
        'data': data
    }
    return render(req, "booktable.html", context)


def bookedit(req, Bid):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = BookCategoryDB.objects.all()
    cat = LibraryBooksDB.objects.get(id=Bid)
    return render(req, "bookedit.html", {'data': data, 'cat': cat})


def UpdateBooks(req, Bid):
    if req.method == "POST":
        bname = req.POST.get('bname')
        genre = req.POST.get('genre')
        auhtor = req.POST.get('author')
        price = req.POST.get('price')
        description = req.POST.get('description')
        try:
            img = req.FILES['b_img']
            fs = FileSystemStorage()
            b_img = fs.save(img.name, img)
        except MultiValueDictKeyError:
            b_img = LibraryBooksDB.objects.get(id=Bid).b_img
        LibraryBooksDB.objects.filter(id=Bid).update(bname=bname, genre=genre, price=price, description=description,
                                                     b_img=b_img, author=auhtor)
        messages.success(req, "updated successfully")
    return redirect(booktable)


def DeleteBook(req, Bid):
    data = LibraryBooksDB.objects.filter(id=Bid)
    data.delete()
    messages.error(req, "Deleted successfully")
    return redirect(booktable)


def LoginPage(req):
    return render(req, "adminlogin.html")


def AdminLogin(req):
    if req.method == "POST":
        username = req.POST.get('user')
        password = req.POST.get('password')
        if User.objects.filter(username__contains=username).exists():
            x = authenticate(req, username=username, password=password)
            if x is not None:
                login(req, x)
                req.session['user'] = username
                messages.success(req, "login successfull")
                return redirect('home')
            else:
                messages.warning(req, "invalid Username or Password")
                return redirect('LoginPage')
        else:
            messages.warning(req, "User not found..!")
            return redirect('LoginPage')


def AdminLogout(req):
    del req.session['user']
    return redirect(LoginPage)


def Membership(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = TempMembership.objects.all()
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
        'alert': alert,
        'reqr': reqr,
        'req_no': req_no,
        'data': data
    }
    return render(req, "membership.html", context)


def MembershipApproval(req):
    if req.method == "POST":
        username = req.POST.get('name')
        password = req.POST.get('password')
        email = req.POST.get('email')
        phone = req.POST.get('phone')
        dob = req.POST.get('dob')
        id = req.POST.get('id')
        message = ("Dear user your request for membership in library has been approved"
                   " you can no login using your username and password")
        sub = "Library membership"
        obj = LibraryMembersDB(username=username, password=password, email=email, phone=phone, dob=dob)
        obj.save()
        send_mail(sub, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        data = TempMembership.objects.filter(id=id)
        data.delete()
        return redirect(Membership)


def RemoveMembership(req,Id):
    data = TempMembership.objects.filter(id=Id)
    data.delete()
    messages.error(req, "Deleted successfully")
    return redirect(Membership)

def MembershipTable(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = LibraryMembersDB.objects.all()
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
        'alert': alert,
        'reqr': reqr,
        'req_no': req_no,
        'data': data
    }
    return render(req, "membertable.html", context)


def MemberEdit(req, Mid):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = LibraryMembersDB.objects.get(id=Mid)
    return render(req, "memberedit.html", {'data': data})


def UpdateMembership(req, Mid):
    if req.method =="POST":
        name = req.POST.get('name')
        email = req.POST.get('email')
        password = req.POST.get('password')
        phone = req.POST.get('phone')
        dob = req.POST.get('dob')
        if LibraryMembersDB.objects.filter(username=name).exclude(id=Mid).exists():
            messages.warning(req, "Username already exists..!")
        elif LibraryMembersDB.objects.filter(email=email).exclude(id=Mid).exists():
            messages.warning(req, "Email already in exists..!")
        else:
            obj = LibraryMembersDB.objects.filter(id=Mid).update(username=name, email=email, password=password, phone=phone, dob=dob)
            messages.success(req, "Details updated successfully..!")
        return redirect(MembershipTable)


def DeleteMember(req, Mid):
    data = LibraryMembersDB.objects.filter(id=Mid)
    data.delete()
    messages.error(req, "Deleted successfully")
    return redirect(MembershipTable)


def ReservationTable(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = Booking.objects.all()
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
        'alert': alert,
        'reqr': reqr,
        'req_no': req_no,
        'data': data
    }
    return render(req, "reservations.html", context)


def Member(req, ID):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = LibraryMembersDB.objects.filter(id=ID)
    return render(req, "membertable.html", {'data': data})


def Book(req, ID):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = LibraryBooksDB.objects.filter(id=ID)
    return render(req, "booktable.html", {'data': data})


def records(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    today = datetime.date.today()
    records = BookRecords.objects.all()
    due = 0
    for i in records:
        if i.return_date and i.return_date.date() < today and i.status != "Returned":
            i.status = "Due"
            i.save()
        elif i.return_date and i.return_date.date() == today and i.status != "Returned":
            email_sent = SentEmail.objects.filter(book_record=i,user=i.user).exists()
            if not email_sent:
                email = i.user.email
                book_name = i.book.bname
                message = (f"Dear member, \n\n"
                           f"The due date for returning the book '{book_name}' is today. "
                           "Please return it to avoid any late fees. \n\n"
                           "Thank you for using our library services.")
                sub = "Library Due Date Reminder"
                send_mail(sub, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                SentEmail.objects.create(user=i.user, book_record=i)
                obj = NotificationDB(user=i.user, records=i, message=message, sub=sub)
                obj.save()

    pending_books = BookRecords.objects.filter(status="pending")
    due_books = BookRecords.objects.filter(status="Due")
    returned_books = BookRecords.objects.filter(status="Returned")
    data = list(due_books) + list(pending_books) + list(returned_books)
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
        'alert': alert,
        'reqr': reqr,
        'req_no': req_no,
        'data': data
    }
    return render(req, "records.html", context)


def SaveRecords(req):
    if req.method == "POST":
        orderid = req.POST.get('orderid')
        data = Booking.objects.get(orderid=orderid)
        user = data.user
        book = data.book
        orderid = orderid
        return_date = data.return_date
        status = "pending"
        Cdate = datetime.datetime.now()
        obj = BookRecords(user=user, book=book, orderid=orderid, return_date=return_date, status=status, collected_time=Cdate)
        obj.save()
        data.delete()
        return redirect(ReservationTable)


def ReturnBook(req, ID):
    Rdate = datetime.datetime.now()
    status = "Returned"
    BookRecords.objects.filter(orderid=ID).update(returned_date=Rdate, status=status)
    record = BookRecords.objects.filter(orderid=ID).first()
    book_name = record.book.bname
    email = record.user.email
    message = (f"Dear member, \n\n"
               f"We have received the book '{book_name}' that you returned. "
               "Thank you for returning it on time. We hope you had a great experience with it. \n\n"
               "If you have any other books to return or need assistance, feel free to contact us. "
               "Thank you for using our library services.")

    sub = "Book Return Notification"
    send_mail(sub, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    obj = NotificationDB(user=record.user, records=record, message=message, sub=sub)
    obj.save()
    return redirect(records)


def notify(req, ID):
    record = BookRecords.objects.filter(orderid=ID).first()
    user = record.user
    email = record.user.email
    book_name = record.book.bname
    message = (f"Dear member, \n\n"
               f"The due date for returning the book '{book_name}' has passed. "
               "Please return it as soon as possible to avoid additional late fees. \n\n"
               "Thank you for using our library services.")

    sub = "Library 'Book Due' Date Reminder"
    send_mail(sub, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    obj = NotificationDB(user=user, records=record, message=message, sub=sub)
    obj.save()
    ob = BookRecords.objects.filter(orderid=ID).update(notification=True)
    return redirect(records)


def MessagePage(req):
    if 'user' not in req.session:
        messages.warning(req, "You need to log in first.")
        return redirect('LoginPage')

    data = ContactDB.objects.all()
    m_req = TempMembership.objects.all()
    req_no = 0
    reqr = 0
    for i in m_req:
        req_no = req_no + 1
    reserve = Booking.objects.all()
    for i in reserve:
        reqr = reqr + 1
    alert = reqr + req_no
    context = {
         'alert': alert,
         'reqr': reqr,
         'req_no': req_no,
         'data': data
    }
    return render(req, "messages.html", context)

def DeleteMessages(req, ID):
    data = ContactDB.objects.filter(id=ID)
    data.delete()
    messages.warning(req, "Message Deleted...!")
    return redirect(MessagePage)