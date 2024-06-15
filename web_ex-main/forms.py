from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SelectMultipleField, IntegerField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, DataRequired, URL, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf.file import FileField, FileAllowed
from models import User, Book, Review, Genre, Cover, Role, book_genres, Collection, book_collections
import bleach

# Кастомное поле для выбора нескольких элементов с помощью чекбоксов
class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

# Форма для авторизации пользователя
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')

# Форма для регистрации пользователя
class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[InputRequired(), Length(min=6, max=100)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=8, max=100)])
    last_name = StringField('Фамилия', validators=[InputRequired(), Length(min=2, max=100)])
    first_name = StringField('Имя', validators=[InputRequired(), Length(min=2, max=100)])
    middle_name = StringField('Отчество', validators=[Length(max=100)])

    # Валидация поля username для проверки уникальности
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такой логин уже занят. Пожалуйста, выберите другой.')

# Форма для добавления новой книги
class BookForm(FlaskForm):
    title = StringField('Название книги', validators=[InputRequired(), Length(max=255)])
    short_description = TextAreaField('Краткое описание книги', validators=[InputRequired()])
    year = IntegerField('Год издания', validators=[InputRequired()])
    publisher = StringField('Издательство', validators=[InputRequired(), Length(max=255)])
    author = StringField('Автор', validators=[InputRequired(), Length(max=255)])
    page_count = IntegerField('Объём (в страницах)', validators=[InputRequired()])
    genre = MultiCheckboxField('Жанр')
    cover_image = FileField('Обложка книги', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Только изображения!')])

    # Инициализация формы и установка значений для поля genre
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.genre.choices = [(genre.id, genre.name) for genre in Genre.query.all()]

# Форма для редактирования информации о книге
class EditBookForm(FlaskForm):
    title = StringField('Название книги', validators=[InputRequired(), Length(min=1, max=255)])
    short_description = TextAreaField('Краткое описание книги', validators=[InputRequired()])
    year = IntegerField('Год издания', validators=[InputRequired()])
    publisher = StringField('Издательство', validators=[InputRequired(), Length(min=1, max=255)])
    author = StringField('Автор', validators=[InputRequired(), Length(min=1, max=255)])
    page_count = IntegerField('Объём (в страницах)', validators=[InputRequired()])
    genre = MultiCheckboxField('Жанр', coerce=int)

    # Инициализация формы и установка значений для поля genre
    def __init__(self, *args, **kwargs):
        super(EditBookForm, self).__init__(*args, **kwargs)
        self.genre.choices = [(genre.id, genre.name) for genre in Genre.query.all()]

    # Метод для заполнения объекта книги данными из формы
    def populate_obj(self, book):
        self.title.populate_obj(book, 'title')
        self.short_description.populate_obj(book, 'short_description')
        self.year.populate_obj(book, 'year')
        self.publisher.populate_obj(book, 'publisher')
        self.author.populate_obj(book, 'author')
        self.page_count.populate_obj(book, 'page_count')
        book.genres = Genre.query.filter(Genre.id.in_(self.genre.data)).all()

    # Валидация жанра для проверки корректности значений
    def validate_genre(self, field):
        genre_ids = [genre.id for genre in Genre.query.all()]
        for genre_id in field.data:
            if genre_id not in genre_ids:
                raise ValidationError('Неверное значение жанра.')

# Форма для добавления рецензии на книгу
class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[
        ('5', 'отлично (значение по умолчанию)'),
        ('4', 'хорошо'),
        ('3', 'удовлетворительно'),
        ('2', 'неудовлетворительно'),
        ('1', 'плохо'),
        ('0', 'ужасно')
    ], validators=[InputRequired()])
    text = TextAreaField('Текст рецензии', validators=[InputRequired(), Length(min=5, max=1000)])
    submit = SubmitField('Оставить рецензию')

# Форма для создания новой подборки
class CollectionForm(FlaskForm):
    title = StringField('Название подборки', validators=[InputRequired(), Length(min=1, max=255)])

# Форма для добавления книги в подборку
class AddToCollectionForm(FlaskForm):
    collection = SelectField('Выберите подборку', coerce=int, validators=[InputRequired()])
