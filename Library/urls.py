from django.urls import path

from Library import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('MemberLogin/', views.MemberLogin, name="MemberLogin"),
    path('MemberSignup/', views.MemberSignup, name="MemberSignup"),
    path('Signup/', views.Signup, name="Signup"),
    path('Login/', views.Login, name="Login"),
    path('logout/', views.logout, name="logout"),
    path('ShopPage/', views.ShopPage, name="ShopPage"),
    path('SingleBook/<int:Id>', views.SingleBook, name="SingleBook"),
    path('CategoryPage/<gn>', views.CategoryPage, name="CategoryPage"),
    path('Review/<int:Id>', views.Review, name="Review"),
    path('updateReview/<int:Id>/<int:bid>/', views.updateReview, name="updateReview"),
    path('SearchCategory/', views.SearchCategory, name="SearchCategory"),
    path('ReserveBook/', views.ReserveBook, name="ReserveBook"),
    path('BorrowRecords/', views.BorrowRecords, name="BorrowRecords"),
    path('ContactPage/', views.ContactPage, name="ContactPage"),
    path('SaveContact/', views.SaveContact, name="SaveContact"),
    path('AboutPage/', views.AboutPage, name="AboutPage"),
    path('Notification/<uname>', views.Notification, name="Notification"),
    path('deleteNotification/<int:ID>', views.deleteNotification, name="deleteNotification"),
]