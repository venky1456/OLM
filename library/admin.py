from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Category, Book, IssueTransaction, BookRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'contact_number', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    ordering = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'status', 'available_copies', 'total_copies', 'publication_year')
    list_filter = ('status', 'category', 'publication_year', 'created_at')
    search_fields = ('title', 'author', 'isbn', 'publisher')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('title',)
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'category', 'description')
        }),
        ('Publication Details', {
            'fields': ('publication_year', 'publisher')
        }),
        ('Inventory', {
            'fields': ('total_copies', 'available_copies', 'status')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(IssueTransaction)
class IssueTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'book', 'student', 'status', 'issue_date', 'due_date', 'return_date', 'fine_amount')
    list_filter = ('status', 'issue_date', 'due_date', 'return_date')
    search_fields = ('transaction_id', 'book__title', 'student__username', 'student__first_name', 'student__last_name')
    readonly_fields = ('transaction_id', 'issue_date', 'fine_amount')
    ordering = ('-issue_date',)
    list_per_page = 25
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_id', 'book', 'student', 'issued_by')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'return_date')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Financial', {
            'fields': ('fine_amount',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('book', 'student', 'issued_by')

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'status', 'request_date', 'processed_by', 'processed_date')
    list_filter = ('status', 'request_date', 'processed_date')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'book__title')
    readonly_fields = ('request_date',)
    ordering = ('-request_date',)
    list_per_page = 20
    
    fieldsets = (
        ('Request Information', {
            'fields': ('student', 'book', 'request_date')
        }),
        ('Processing', {
            'fields': ('status', 'processed_by', 'processed_date', 'notes')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('student', 'book', 'processed_by')

# Customize admin site
admin.site.site_header = "Online Library Management System"
admin.site.site_title = "OLMS Admin"
admin.site.index_title = "Welcome to OLMS Administration"
