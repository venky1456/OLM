from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class UserProfile(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Book(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('issued', 'Issued'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    )
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    description = models.TextField(blank=True, null=True)
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2025)],
        blank=True, null=True
    )
    publisher = models.CharField(max_length=200, blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def is_available(self):
        return self.available_copies > 0 and self.status == 'available'
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']

class IssueTransaction(models.Model):
    STATUS_CHOICES = (
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
    )
    
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_issues')
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_issued', blank=True, null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='issued')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.student.username} - {self.status}"
    
    def is_overdue(self):
        from django.utils import timezone
        return self.status == 'issued' and timezone.now() > self.due_date
    
    def calculate_fine(self):
        from django.utils import timezone
        if self.status == 'issued' and timezone.now() > self.due_date:
            days_overdue = (timezone.now() - self.due_date).days
            return days_overdue * 1.00  # $1 per day
        return 0.00
    
    class Meta:
        verbose_name = "Issue Transaction"
        verbose_name_plural = "Issue Transactions"
        ordering = ['-issue_date']

class BookRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_requests')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_requests', blank=True, null=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.book.title} - {self.status}"
    
    class Meta:
        verbose_name = "Book Request"
        verbose_name_plural = "Book Requests"
        ordering = ['-request_date']
