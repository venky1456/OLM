from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Book, Category, IssueTransaction, BookRequest
from django.utils import timezone
from datetime import timedelta

class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES, initial='student')
    
    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name'].split()[0]
        user.last_name = ' '.join(self.cleaned_data['full_name'].split()[1:]) if len(self.cleaned_data['full_name'].split()) > 1 else ''
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type'],
                contact_number=self.cleaned_data['contact_number'],
                address=self.cleaned_data['address']
            )
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'description', 'publication_year', 'publisher', 'total_copies', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()
            # Set available copies equal to total copies for new books
            book.available_copies = book.total_copies
            book.save()
        return book

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class IssueBookForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__user_type='student'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Student'
    )
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(status='available', available_copies__gt=0),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Book'
    )
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        initial=lambda: timezone.now() + timedelta(days=14)  # Default 14 days
    )
    
    class Meta:
        model = IssueTransaction
        fields = ['student', 'book', 'due_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def save(self, commit=True, issued_by=None):
        transaction = super().save(commit=False)
        transaction.issued_by = issued_by
        if commit:
            transaction.save()
            # Update book availability
            book = transaction.book
            book.available_copies -= 1
            if book.available_copies == 0:
                book.status = 'issued'
            book.save()
        return transaction

class ReturnBookForm(forms.ModelForm):
    return_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        initial=timezone.now,
        label='Return Date'
    )
    fine_amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label='Fine Amount ($)'
    )
    
    class Meta:
        model = IssueTransaction
        fields = ['return_date', 'fine_amount', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction.status = 'returned'
        transaction.return_date = self.cleaned_data['return_date']
        transaction.fine_amount = self.cleaned_data['fine_amount'] or 0
        
        if commit:
            transaction.save()
            # Update book availability
            book = transaction.book
            book.available_copies += 1
            if book.status == 'issued':
                book.status = 'available'
            book.save()
        return transaction

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional notes for your request...'}),
        }

class BookSearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('title', 'Title'),
        ('author', 'Author'),
        ('isbn', 'ISBN'),
        ('category', 'Category'),
    )
    
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, initial='title', widget=forms.Select(attrs={'class': 'form-control'}))
    search_query = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter search term...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'})) 