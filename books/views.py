from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, CartItem, City
from users.models import Profile
import requests
import json
from decimal import Decimal

def book_list(request):
    query = request.GET.get('q', '')
    city_name = request.GET.get('city', '')
    books = []
    
    if query:
        # Search Google Books API
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'items' in data:
                for item in data['items']:
                    volume_info = item.get('volumeInfo', {})
                    
                    # Extract book details
                    google_id = item.get('id', '')
                    title = volume_info.get('title', 'Unknown Title')
                    authors = volume_info.get('authors', ['Unknown Author'])
                    author = authors[0] if authors else 'Unknown Author'
                    description = volume_info.get('description', '')
                    
                    # Get image URL if available
                    image_links = volume_info.get('imageLinks', {})
                    image_url = image_links.get('thumbnail', '')
                    
                    # Get or create book in database
                    book, created = Book.objects.get_or_create(
                        google_id=google_id,
                        defaults={
                            'title': title,
                            'author': author,
                            'description': description,
                            'image': image_url,
                            'price': Decimal('9.99')  # Default price
                        }
                    )
                    
                    # If book exists but we have new data, update it
                    if not created:
                        book.title = title
                        book.author = author
                        book.description = description
                        if image_url:
                            book.image = image_url
                        book.save()
                    
                    # Add to available cities if city is specified
                    if city_name:
                        try:
                            city, _ = City.objects.get_or_create(name=city_name)
                            book.available_cities.add(city)
                        except Exception as e:
                            print(f"Error adding city: {e}")
                    
                    books.append(book)
            else:
                messages.info(request, "No books found for your search.")
        else:
            messages.error(request, "Error connecting to book service. Please try again later.")
    
    # Filter by city if specified
    if city_name and books:
        try:
            city = City.objects.get(name__iexact=city_name)
            filtered_books = []
            for book in books:
                if city in book.available_cities.all():
                    filtered_books.append(book)
            books = filtered_books
            
            if not books:
                messages.warning(request, f"No books found in {city_name}")
        except City.DoesNotExist:
            messages.warning(request, f"No stores found in {city_name}")
    
    context = {
        'books': books,
        'query': query,
        'city_name': city_name
    }
    
    return render(request, 'books/book_list.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    
    return render(request, 'books/cart.html', context)

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{book.title} added to your cart!")
    return redirect('book_detail', book_id=book_id)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    
    messages.success(request, f"{cart_item.book.title} removed from your cart!")
    return redirect('cart')
