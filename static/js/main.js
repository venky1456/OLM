// Main JavaScript for Online Library Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFormValidation();
    initializeSearchFunctionality();
    initializeTooltips();
    initializeConfirmDialogs();
    initializeAutoHideAlerts();
    initializeBookSearch();
});

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Search Functionality
function initializeSearchFunctionality() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else {
                clearSearchResults();
            }
        });
    }
}

// AJAX Book Search
function performSearch(query) {
    const searchResults = document.getElementById('search-results');
    if (!searchResults) return;
    
    // Show loading spinner
    searchResults.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div></div>';
    searchResults.style.display = 'block';
    
    fetch(`/search-books-ajax/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.books, searchResults);
        })
        .catch(error => {
            console.error('Search error:', error);
            searchResults.innerHTML = '<div class="alert alert-danger">Error performing search</div>';
        });
}

function displaySearchResults(books, container) {
    if (books.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No books found</div>';
        return;
    }
    
    const resultsHtml = books.map(book => `
        <div class="list-group-item list-group-item-action">
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${book.title}</h6>
                <small class="text-muted">${book.author}</small>
            </div>
            <a href="/books/${book.id}/" class="btn btn-sm btn-primary mt-2">View Details</a>
        </div>
    `).join('');
    
    container.innerHTML = `
        <div class="list-group">
            ${resultsHtml}
        </div>
    `;
}

function clearSearchResults() {
    const searchResults = document.getElementById('search-results');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}

// Book Search with Filters
function initializeBookSearch() {
    const searchForm = document.getElementById('book-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const params = new URLSearchParams();
            
            for (let [key, value] of formData.entries()) {
                if (value) {
                    params.append(key, value);
                }
            }
            
            // Redirect to search results
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    }
}

// Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Confirmation Dialogs
function initializeConfirmDialogs() {
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Auto-hide Alerts
function initializeAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Book Availability Check
function checkBookAvailability(bookId) {
    fetch(`/api/book-availability/${bookId}/`)
        .then(response => response.json())
        .then(data => {
            const availabilityElement = document.getElementById(`availability-${bookId}`);
            if (availabilityElement) {
                availabilityElement.textContent = data.available ? 'Available' : 'Not Available';
                availabilityElement.className = data.available ? 'badge bg-success' : 'badge bg-danger';
            }
        })
        .catch(error => {
            console.error('Error checking availability:', error);
        });
}

// Form Enhancement Functions
function enhanceFormFields() {
    // Add character counters to textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const counter = document.createElement('small');
        counter.className = 'form-text text-muted';
        counter.id = `${textarea.id}-counter`;
        textarea.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = textarea.maxLength - textarea.value.length;
            counter.textContent = `${remaining} characters remaining`;
        }
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
}

// Table Enhancement
function enhanceTables() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        // Add zebra striping
        table.classList.add('table-striped');
        
        // Add hover effect
        table.classList.add('table-hover');
        
        // Make tables responsive
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
}

// Pagination Enhancement
function enhancePagination() {
    const pagination = document.querySelector('.pagination');
    if (pagination) {
        pagination.classList.add('justify-content-center');
    }
}

// Loading States
function showLoading(element) {
    if (element) {
        element.disabled = true;
        const originalText = element.textContent;
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        element.setAttribute('data-original-text', originalText);
    }
}

function hideLoading(element) {
    if (element) {
        element.disabled = false;
        const originalText = element.getAttribute('data-original-text');
        if (originalText) {
            element.textContent = originalText;
        }
    }
}

// Utility Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Export Functions
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        let row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            let text = cols[j].innerText.replace(/"/g, '""');
            row.push('"' + text + '"');
        }
        
        csv.push(row.join(','));
    }
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Print Functions
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Print</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    @media print {
                        .no-print { display: none !important; }
                    }
                </style>
            </head>
            <body>
                ${element.outerHTML}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Initialize all enhancements
document.addEventListener('DOMContentLoaded', function() {
    enhanceFormFields();
    enhanceTables();
    enhancePagination();
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
}); 