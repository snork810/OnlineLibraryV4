from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from books.models import NoModeratedBooksModel

def home(request):
   return render(request, 'djangolib/home.html')

def library(request):
    books = EBooksModel.objects.order_by('author')
    for book in books:
        book.available_formats = []
        if book.fb2:
            book.available_formats.append('fb2')
        if book.txt:
            book.available_formats.append('txt')
        if book.epub:
            book.available_formats.append('epub')

    user_favourite_ids = FavouriteBook.objects.filter(user=request.user).values_list('book_id', flat=True)  # Получаем только ID
    context = {
        'books': books,
        'user_favourite_ids': user_favourite_ids,  # Передаем IDs в контекст
    }
    return render(request, 'djangolib/library.html', context)

def approve_books(request):
    books = NoModeratedBooksModel.objects.all()

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = NoModeratedBooksModel.objects.get(pk=book_id)
        author_name = book.author  # Предполагаем, что в NoModeratedBooksModel хранится имя автора
        author, created = Author.objects.get_or_create(name=author_name, bio=f'Добавлен пользователем {request.user.username}')
        approved_book = EBooksModel.objects.create(
            title=book.title,
            summary=book.summary,
            pages=book.pages,
            fb2=book.fb2,
            author=author,
            cover_image=book.cover_image,
            category=book.category
        )

        favorite_book = FavouriteBook(user=request.user, book=approved_book)
        favorite_book.save()
        book.delete()
        return redirect('approve_books')

    context = {
        'books': books
    }
    return render(request, 'djangolib/approve_books.html', context)


def download_file(request, book_id):
    book = get_object_or_404(EBooksModel, id=book_id)

    selected_format = request.POST.get('format', 'txt')

    if selected_format == 'epub':
        file_path = book.epub.path
        content_type = 'application/octet-stream'
        file_name = f"{book.title}.epub"
    elif selected_format == 'fb2':
        file_path = book.fb2.path
        content_type = 'application/octet-stream'
        file_name = f"{book.title}.fb2"
    else:
        file_path = book.txt.path
        content_type = 'application/octet-stream'
        file_name = f"{book.title}.txt"

    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response




def file_detail_lib(request, pk):
    file_instance = get_object_or_404(EBooksModel, pk=pk)
    RecentlyOpened.objects.get_or_create(user=request.user, book=file_instance)
    file_path = file_instance.fb2.path
    content_type = 'application/x-fictionbook+xml'
    file_name = f"{file_instance.title}.fb2"
    response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{file_name}"'  # 'inline' разрешает открытие в браузере
    return response


@login_required
def add_to_favorites(request, book_id):
    book = EBooksModel.objects.get(id=book_id)
    if request.method == 'POST':
        favorite_book = FavouriteBook(user=request.user, book=book)
        favorite_book.save()
        return redirect('bookshelf')

    return render(request, 'djangolib/library.html', {'book': book})