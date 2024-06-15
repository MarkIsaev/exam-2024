document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы кнопки открытия модального окна, самого модального окна и кнопки закрытия
    const addToCollectionBtn = document.getElementById('addToCollectionBtn');
    const addToCollectionModal = document.getElementById('addToCollectionModal');
    const closeModal = document.querySelector('.close');

    // Проверяем, существуют ли элементы на странице
    if (addToCollectionBtn && addToCollectionModal && closeModal) {
        // Добавляем обработчик события клика на кнопку открытия модального окна
        addToCollectionBtn.addEventListener('click', function() {
            addToCollectionModal.style.display = 'block'; // Показываем модальное окно
        });

        // Добавляем обработчик события клика на кнопку закрытия модального окна
        closeModal.addEventListener('click', function() {
            addToCollectionModal.style.display = 'none'; // Скрываем модальное окно
        });

        // Добавляем обработчик события клика по окну
        window.addEventListener('click', function(event) {
            if (event.target === addToCollectionModal) { // Проверяем, что клик был вне модального окна
                addToCollectionModal.style.display = 'none'; // Скрываем модальное окно
            }
        });
    }

    // Обрабатываем чекбоксы жанров, устанавливая их значение на основе данных из скрытого поля
    const selectedGenresInput = document.getElementById('selectedGenres');
    if (selectedGenresInput) {
        const selectedGenres = JSON.parse(selectedGenresInput.value); // Преобразуем JSON-строку в массив
        selectedGenres.forEach(function(genreId) {
            const checkbox = document.getElementById("genre-" + genreId); // Находим чекбокс по ID жанра
            if (checkbox) {
                checkbox.checked = true; // Устанавливаем чекбокс в состояние "выбран"
            }
        });
    }

    // Инициализация редактора EasyMDE для поля описания книги
    const descriptionElement = document.getElementById("short_description");
    if (descriptionElement) {
        new EasyMDE({ element: descriptionElement }); // Создаем новый экземпляр редактора
    }

    // Инициализация редактора EasyMDE для поля текста рецензии
    const reviewTextElement = document.getElementById("review-text");
    if (reviewTextElement) {
        const reviewMDE = new EasyMDE({
            element: reviewTextElement,
            forceSync: true, // Принудительная синхронизация значения поля с текстом редактора
            spellChecker: false, // Отключаем проверку орфографии
            autosave: {
                enabled: false, // Отключаем автосохранение
            },
        });

        // Добавляем обработчик события изменения содержимого редактора
        reviewMDE.codemirror.on("change", function(){
            reviewTextElement.value = reviewMDE.value(); // Обновляем значение текстового поля
        });
    }
});
