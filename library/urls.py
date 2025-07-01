from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Book Management (Admin)
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # Student Book Views
    path('student/books/', views.student_book_list, name='student_book_list'),
    path('student/books/<int:book_id>/request/', views.request_book, name='request_book'),
    
    # Issue/Return Management
    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/<uuid:transaction_id>/', views.return_book, name='return_book'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    
    # Category Management
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    
    # Book Request Management (Admin)
    path('book-requests/', views.book_request_list, name='book_request_list'),
    path('book-requests/<int:request_id>/approve/', views.approve_book_request, name='approve_book_request'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # AJAX
    path('search-books-ajax/', views.search_books_ajax, name='search_books_ajax'),
] 