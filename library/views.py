from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, Book, Category, IssueTransaction, BookRequest
from .forms import (
    UserRegistrationForm, UserLoginForm, BookForm, CategoryForm,
    IssueBookForm, ReturnBookForm, BookRequestForm, BookSearchForm, ContactForm
)

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type == 'admin'

def is_student(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type == 'student'

# Home Page
def home(request):
    recent_books = Book.objects.filter(status='available')[:6]
    total_books = Book.objects.count()
    total_students = User.objects.filter(profile__user_type='student').count()
    total_issues = IssueTransaction.objects.filter(status='issued').count()
    
    context = {
        'recent_books': recent_books,
        'total_books': total_books,
        'total_students': total_students,
        'total_issues': total_issues,
    }
    return render(request, 'home.html', context)

# Authentication Views
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# Dashboard Views
@login_required
def dashboard(request):
    if is_admin(request.user):
        return admin_dashboard(request)
    elif is_student(request.user):
        return student_dashboard(request)
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('home')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_students = User.objects.filter(profile__user_type='student').count()
    active_issues = IssueTransaction.objects.filter(status='issued').count()
    overdue_books = IssueTransaction.objects.filter(status='issued').filter(due_date__lt=timezone.now()).count()
    
    recent_transactions = IssueTransaction.objects.all()[:10]
    recent_requests = BookRequest.objects.filter(status='pending')[:5]
    
    context = {
        'total_books': total_books,
        'total_students': total_students,
        'active_issues': active_issues,
        'overdue_books': overdue_books,
        'recent_transactions': recent_transactions,
        'recent_requests': recent_requests,
    }
    return render(request, 'dashboard_admin.html', context)

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    user_issues = IssueTransaction.objects.filter(student=request.user, status='issued')
    user_history = IssueTransaction.objects.filter(student=request.user).exclude(status='issued')[:10]
    user_requests = BookRequest.objects.filter(student=request.user)[:5]
    
    context = {
        'user_issues': user_issues,
        'user_history': user_history,
        'user_requests': user_requests,
    }
    return render(request, 'dashboard_student.html', context)

# Book Management Views
@login_required
@user_passes_test(is_admin)
def book_list(request):
    search_form = BookSearchForm(request.GET)
    books = Book.objects.all()
    
    if search_form.is_valid():
        search_type = search_form.cleaned_data.get('search_type')
        search_query = search_form.cleaned_data.get('search_query')
        category = search_form.cleaned_data.get('category')
        
        if search_query:
            if search_type == 'title':
                books = books.filter(title__icontains=search_query)
            elif search_type == 'author':
                books = books.filter(author__icontains=search_query)
            elif search_type == 'isbn':
                books = books.filter(isbn__icontains=search_query)
            elif search_type == 'category':
                books = books.filter(category__name__icontains=search_query)
        
        if category:
            books = books.filter(category=category)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'categories': Category.objects.all(),
    }
    return render(request, 'book_list.html', context)

@login_required
@user_passes_test(is_admin)
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'book_form.html', {'form': form, 'title': 'Add New Book'})

@login_required
@user_passes_test(is_admin)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'book_form.html', {'form': form, 'title': 'Edit Book', 'book': book})

@login_required
@user_passes_test(is_admin)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'book_confirm_delete.html', {'book': book})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_available = book.is_available()
    
    context = {
        'book': book,
        'is_available': is_available,
    }
    return render(request, 'book_detail.html', context)

# Student Book Views
@login_required
@user_passes_test(is_student)
def student_book_list(request):
    search_form = BookSearchForm(request.GET)
    books = Book.objects.filter(status='available', available_copies__gt=0)
    
    if search_form.is_valid():
        search_type = search_form.cleaned_data.get('search_type')
        search_query = search_form.cleaned_data.get('search_query')
        category = search_form.cleaned_data.get('category')
        
        if search_query:
            if search_type == 'title':
                books = books.filter(title__icontains=search_query)
            elif search_type == 'author':
                books = books.filter(author__icontains=search_query)
            elif search_type == 'isbn':
                books = books.filter(isbn__icontains=search_query)
            elif search_type == 'category':
                books = books.filter(category__name__icontains=search_query)
        
        if category:
            books = books.filter(category=category)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'categories': Category.objects.all(),
    }
    return render(request, 'student_book_list.html', context)

@login_required
@user_passes_test(is_student)
def request_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.student = request.user
            book_request.book = book
            book_request.save()
            messages.success(request, 'Book request submitted successfully!')
            return redirect('student_book_list')
    else:
        form = BookRequestForm()
    
    return render(request, 'request_book.html', {'form': form, 'book': book})

# Issue/Return Management
@login_required
@user_passes_test(is_admin)
def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            form.save(issued_by=request.user)
            messages.success(request, 'Book issued successfully!')
            return redirect('admin_dashboard')
    else:
        form = IssueBookForm()
    
    return render(request, 'issue_book.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def return_book(request, transaction_id):
    transaction = get_object_or_404(IssueTransaction, transaction_id=transaction_id)
    
    if request.method == 'POST':
        form = ReturnBookForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book returned successfully!')
            return redirect('admin_dashboard')
    else:
        form = ReturnBookForm(instance=transaction)
    
    return render(request, 'return_book.html', {
        'form': form, 
        'transaction': transaction,
        'today': timezone.now().date(),
    })

@login_required
@user_passes_test(is_admin)
def transaction_list(request):
    transactions = IssueTransaction.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'today': timezone.now().date(),
    }
    return render(request, 'transaction_list.html', context)

# Category Management
@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'category_form.html', {'form': form, 'title': 'Add New Category'})

@login_required
@user_passes_test(is_admin)
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'category_form.html', {'form': form, 'title': 'Edit Category', 'category': category})

# Contact Page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real application, you would send an email here
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

# AJAX Views for dynamic functionality
def search_books_ajax(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query)
        )[:10]
        data = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
    else:
        data = []
    
    return JsonResponse({'books': data})

# Book Request Management (Admin)
@login_required
@user_passes_test(is_admin)
def book_request_list(request):
    requests = BookRequest.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    paginator = Paginator(requests, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'book_request_list.html', context)

@login_required
@user_passes_test(is_admin)
def approve_book_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action in ['approve', 'reject']:
            book_request.status = 'approved' if action == 'approve' else 'rejected'
            book_request.processed_by = request.user
            book_request.processed_date = timezone.now()
            book_request.notes = notes
            book_request.save()
            
            if action == 'approve':
                messages.success(request, f'Book request for "{book_request.book.title}" has been approved.')
            else:
                messages.success(request, f'Book request for "{book_request.book.title}" has been rejected.')
            
            return redirect('book_request_list')
    
    return render(request, 'book_request_detail.html', {'book_request': book_request})
