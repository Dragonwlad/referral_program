

# Простая реферальная система


## Разворачивание проекта.
- Клонируйте репозиторий.
- Установите виртуальное окружение.
- Установите зависимости (зависимости находятся в файле requiirements.txt)
- Перейдите в папку referral_program и выполните команду "python manage.py runserver"

## Документация
После разворачивания проекта полная документация будет доступна по адресу
http://127.0.0.1:8000/redoc/


# Авторизация
Для получения полного доступа к сервису нужно авторизоваться.

## Регистрация пользователей
Пользователь отправляет POST-запрос на добавление нового пользователя с номером телефона phone_number на эндпоинт /auth/signup/.
Приложение отправляет СМС с кодом подтверждения (confirmation_code) по телефону phone_number.
Пользователь отправляет POST-запрос с параметрами phone_number и confirmation_code на эндпоинт /auth/token//, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт /profile/ и заполняет поле inviter_code.

## Получение токена
Для получения токена необходимо на адрес
http://127.0.0.1:8000/api/v1/auth/token/ отправить имя пользователя и токен:
{
"phone_number": "string",
"confirmation_code": "string"
}
В ответ вам придет уникальный токен пользователя.

## Автор
Владислав Кузнецов
