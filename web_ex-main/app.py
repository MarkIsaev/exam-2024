from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from extensions import db, migrate, login_manager
from forms import LoginForm, RegisterForm
from books import books as books_blueprint
from collections_blueprint import collections_bp as collections_blueprint
from models import User, Book, Review, Genre, Cover, Role, book_genres, Collection, book_collections
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

def create_app():
    # Создаем экземпляр приложения Flask
    app = Flask(__name__)
    # Загружаем конфигурацию из объекта Config
    app.config.from_object(Config)

    # Инициализация расширений с приложением Flask
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Устанавливаем представление для страницы входа

    # Регистрация блюпринтов (Blueprints)
    app.register_blueprint(books_blueprint)
    app.register_blueprint(collections_blueprint, url_prefix='/collections')

    # Загрузчик пользователя для Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Маршрут для главной страницы
    @app.route('/')
    @app.route('/index')
    def index():
        # Пагинация для отображения книг на страницах
        page = request.args.get('page', 1, type=int)
        books = Book.query.order_by(Book.year.desc()).paginate(page=page, per_page=10, error_out=False)

        # Рассчитываем средний рейтинг и количество отзывов для каждой книги
        for book in books.items:
            reviews = Review.query.filter_by(book_id=book.id).all()
            if reviews:
                total_ratings = sum(review.rating for review in reviews)
                book.avg_rating = total_ratings / len(reviews)
                book.review_count = len(reviews)
            else:
                book.avg_rating = 0
                book.review_count = 0

        return render_template('index.html', books=books)

    # Маршрут для страницы входа
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Вход успешно выполнен!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Неверное имя пользователя или пароль.', 'danger')

        return render_template('login.html', form=form)

    # Маршрут для страницы регистрации
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Пользователь с таким именем уже существует.', 'danger')
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(username=form.username.data,
                            password=hashed_password,
                            last_name=form.last_name.data,
                            first_name=form.first_name.data,
                            middle_name=form.middle_name.data)

            base_role = Role.query.filter_by(id=3).first()
            new_user.role = base_role

            db.session.add(new_user)
            db.session.commit()

            flash('Регистрация успешно завершена! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    # Маршрут для выхода из системы
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Выход успешно выполнен!', 'success')
        return redirect(url_for('index'))

    # Обработчик ошибок 404 (страница не найдена)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Обработчик ошибок 500 (внутренняя ошибка сервера)
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()  # Создаем приложение
    app.run(debug=True)  # Запускаем сервер в режиме отладки
