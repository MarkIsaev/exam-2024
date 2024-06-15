INSERT INTO roles (name, description) VALUES
    ('admin', 'Администратор (суперпользователь)'),
    ('moderator', 'Модератор (редактирует данные книг и модерирует рецензии)'),
    ('user', 'Пользователь (может оставлять рецензии)');

INSERT INTO genres (name) VALUES
    ('Фантастика'),
    ('Роман'),
    ('Детектив'),
    ('Поэзия'),
    ('Документальная литература'),
    ('Фэнтези'),
    ('Классика'),
    ('Приключения');

INSERT INTO users (username, password, last_name, first_name, middle_name, role_id) VALUES
    ('admin', '12345678', 'Исаев', 'Марк', NULL, 1),
    ('moderator', '12345678', 'Модератор', '---', NULL, 2),
    ('user', '12345678', 'Пользователь', '----', NULL, 3);

INSERT INTO covers (filename, mime_type, md5_hash) VALUES
    ('1.jpeg', 'image/jpeg', '1'),
    ('2.jpeg', 'image/jpeg', '2'),
    ('3.jpeg', 'image/jpeg', '3'),
    ('4.jpeg', 'image/jpeg', '4'),
    ('5.jpeg', 'image/jpeg', '5'),
    ('6.jpeg', 'image/jpeg', '6'),
    ('7.jpeg', 'image/jpeg', '7'),
    ('8.jpeg', 'image/jpeg', '8'),
    ('9.jpeg', 'image/jpeg', '9'),
    ('10.jpeg', 'image/jpeg', '10'),
    ('11.jpeg', 'image/jpeg', '11'),
    ('12.jpeg', 'image/jpeg', '12');

INSERT INTO books (title, short_description, year, publisher, author, page_count, cover_id)
VALUES
    ('Убить пересмешника', 'Роман о расовых предрассудках и морали', 1960, 'АСТ', 'Харпер Ли', 336, 1),
    ('Преступление и наказание', 'Роман о вине и искуплении', 1866, 'Эксмо', 'Фёдор Достоевский', 671, 2),
    ('О дивный новый мир', 'Антиутопия о будущем', 1932, 'Азбука', 'Олдос Хаксли', 311, 3),
    ('Жизнь Пи', 'Роман о выживании', 2001, 'АСТ', 'Янн Мартел', 464, 4),
    ('Сто лет одиночества', 'Магический реализм', 1967, 'Эксмо', 'Габриэль Гарсиа Маркес', 417, 5),
    ('Сияние', 'Хоррор', 1977, 'АСТ', 'Стивен Кинг', 688, 6),
    ('Игра престолов', 'Фэнтези', 1996, 'АСТ', 'Джордж Р. Р. Мартин', 848, 7),
    ('Портрет Дориана Грея', 'Философский роман', 1890, 'Азбука', 'Оскар Уайльд', 288, 8),
    ('Унесённые ветром', 'Исторический роман', 1936, 'Азбука', 'Маргарет Митчелл', 1037, 9),
    ('451 градус по Фаренгейту', 'Антиутопия о будущем', 1953, 'Эксмо', 'Рэй Брэдбери', 256, 10),
    ('Дюна', 'Фантастика', 1965, 'АСТ', 'Фрэнк Герберт', 704, 11),
    ('Человек в высоком замке', 'Альтернативная история', 1962, 'Азбука', 'Филип К. Дик', 274, 12);

INSERT INTO book_genres (book_id, genre_id) VALUES
    (1, 5),  -- Убить пересмешника: Классика
    (2, 5),  -- Преступление и наказание: Классика
    (3, 1),  -- О дивный новый мир: Фантастика
    (4, 5),  -- Жизнь Пи: Классика
    (5, 5),  -- Сто лет одиночества: Классика
    (6, 7),  -- Сияние: Хоррор
    (7, 4),  -- Игра престолов: Фэнтези
    (8, 5),  -- Портрет Дориана Грея: Классика
    (9, 5),  -- Унесённые ветром: Классика
    (10, 1), -- 451 градус по Фаренгейту: Фантастика
    (11, 1), -- Дюна: Фантастика
    (12, 3); -- Человек в высоком замке: Альтернативная история

