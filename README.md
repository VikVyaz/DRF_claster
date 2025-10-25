# Приложение с рассылками

## !!!ВНИМАНИЕ!!!
Прежде ВСЕГО:
* `python manage.py check_db` - для проверки/создания рабочей БД (данные из `.env`)
* `python manage.py create_media` - для создания папки media для превью Курсов и Уроков

### Полезности:
* `python manage.py create_test_payment` - создание тестовых User, Course, Lesson и Payment для быстрого наполнения для проверки работы.
  * При этом запускать можно повторно, тк тестовые Course и Lesson создаются с именами "Тестовый курс/урок_1 (2, 3 и тд)" 
* `python manage.py createadmin` - создание su с кастомными username, email и password из `.env`.
  * По сути аналогично `python manage.py create_test_payment`


## Swagger
* Реализован Swagger
* Авторизация через Bearer-токен
  * Справа вверху от списка эндпоинтов "Authorize" в формате "Bearer <твой токен>"
  * Токен можно получить в get-запросе на utl /users/login/ с введением своего email и password