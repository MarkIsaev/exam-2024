import os
import hashlib
import bleach
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from extensions import db
from forms import BookForm, EditBookForm, ReviewForm
from models import Book, Review, Genre, Cover, Collection
import markdown2

# Создаем блюпринт для книг
books = Blueprint('books', __name__)

@books.route('/book/<int:book_id>')
def book(book_id):
    # Получаем книгу по ID или возвращаем ошибку 404, если она не найдена
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book.id).all()

    user_review = None
    form = ReviewForm()

    collections = []
    if current_user.is_authenticated:
        # Получаем рецензию пользователя, если она существует
        user_review = Review.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        # Получаем все коллекции пользователя
        collections = Collection.query.filter_by(user_id=current_user.id).all()

    # Отображаем страницу книги
    return render_template('book.html', book=book, reviews=reviews, user_review=user_review, form=form, collections=collections)

# Добавляем фильтр для преобразования текста в markdown
@books.app_template_filter('markdown')
def apply_markdown(text):
    return markdown2.markdown(text, extras=['fenced-code-blocks'])

@books.route('/book/<int:book_id>/review', methods=['GET', 'POST'])
@login_required
def review(book_id):
    # Получаем книгу по ID или возвращаем ошибку 404, если она не найдена
    book = Book.query.get_or_404(book_id)
    form = ReviewForm()

    # Проверяем, оставлял ли пользователь уже рецензию на эту книгу
    user_review = Review.query.filter_by(user_id=current_user.id, book_id=book_id).first()

    if user_review:
        flash('Вы уже оставили рецензию для этой книги', 'info')
        return redirect(url_for('books.book', book_id=book_id))

    if form.validate_on_submit():
        try:
            # Очищаем текст рецензии от потенциально опасного HTML
            cleaned_text = bleach.clean(form.text.data, strip=True)
            review = Review(
                rating=form.rating.data,
                text=cleaned_text,
                user_id=current_user.id,
                book_id=book_id
            )
            db.session.add(review)
            db.session.commit()

            flash('Рецензия успешно добавлена', 'success')
            return redirect(url_for('books.book', book_id=book_id))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении рецензии. Пожалуйста, попробуйте еще раз.', 'danger')

    return render_template('review.html', form=form, book=book)

@books.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для выполнения данного действия', 'warning')
        return redirect(url_for('index'))

    form = BookForm()
    form.genre.choices = [(genre.id, genre.name) for genre in Genre.query.all()]

    if form.validate_on_submit():
        try:
            genres = Genre.query.filter(Genre.id.in_(form.genre.data)).all()

            cover_id = None
            if form.cover_image.data:
                file = form.cover_image.data
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()

                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                md5_hash = calculate_md5(file_path)

                existing_cover = Cover.query.filter_by(md5_hash=md5_hash).first()

                if existing_cover:
                    cover_id = existing_cover.id
                    os.remove(file_path)
                else:
                    new_filename = f"{md5_hash}.{file_extension}"
                    new_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
                    os.rename(file_path, new_file_path)

                    mime_type = file.mimetype

                    new_cover = Cover(filename=new_filename, mime_type=mime_type, md5_hash=md5_hash)
                    db.session.add(new_cover)
                    db.session.commit()
                    cover_id = new_cover.id

            cleaned_title = bleach.clean(form.title.data, strip=True)
            cleaned_publisher = bleach.clean(form.publisher.data, strip=True)
            cleaned_author = bleach.clean(form.author.data, strip=True)
            cleaned_description = bleach.clean(form.short_description.data, strip=True)

            book = Book(
                title=cleaned_title,
                short_description=cleaned_description,
                year=form.year.data,
                publisher=cleaned_publisher,
                author=cleaned_author,
                page_count=form.page_count.data,
                cover_id=cover_id,
                genres=genres
            )
            db.session.add(book)
            db.session.commit()

            flash('Книга успешно добавлена!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('При добавлении книги возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            return render_template('add_book.html', form=form)

    return render_template('add_book.html', form=form)

# Функция для расчета MD5-хэша файла
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@books.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    # Получаем книгу по ID или возвращаем ошибку 404, если она не найдена
    book = Book.query.get_or_404(book_id)

    if current_user.role.name == 'user' and current_user.id != book.user_id:
        flash('У вас недостаточно прав для выполнения данного действия', 'warning')
        return redirect(url_for('index'))

    form = EditBookForm()

    if form.validate_on_submit():
        try:
            form.populate_obj(book)

            cleaned_description = bleach.clean(form.short_description.data, strip=True)
            book.short_description = cleaned_description

            db.session.commit()
            flash('Книга успешно обновлена!', 'success')
            return redirect(url_for('books.book', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении книги. Пожалуйста, попробуйте еще раз.', 'danger')

    form.title.data = book.title
    form.short_description.data = book.short_description
    form.year.data = book.year
    form.publisher.data = book.publisher
    form.author.data = book.author
    form.page_count.data = book.page_count

    selected_genres = [genre.id for genre in book.genres]
    form.genre.data = selected_genres

    return render_template('edit_book.html', form=form, book=book, selected_genres=selected_genres)

@books.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    if current_user.role.id != 1:
        flash('У вас недостаточно прав для выполнения данного действия', 'warning')
        return redirect(url_for('index'))

    try:
        book = Book.query.get_or_404(book_id)

        other_book_with_same_cover = Book.query.filter(Book.cover_id == book.cover_id, Book.id != book.id).first()

        if other_book_with_same_cover:
            book.cover_id = None
        else:
            cover = Cover.query.get(book.cover_id)
            if cover:
                cover_path = os.path.join(current_app.config['UPLOAD_FOLDER'], cover.filename)
                if os.path.exists(cover_path):
                    os.remove(cover_path)
                db.session.delete(cover)
                book.cover_id = None

        db.session.delete(book)
        db.session.commit()

        flash('Книга успешно удалена!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении книги. Пожалуйста, попробуйте еще раз.', 'danger')

    return redirect(url_for('index'))
