Для запуска проекта разверните Docker:
Windows:
docker-compose up
Linux
sudo docker-compose up
После примените все миграции:
alembic -c .\alembic\alembic.ini upgrade head

Поздравляю!
Проект запущен, чтобы залогиниться через swagger в полях username и password вбиваем 
username: user1
password 123123123 
и получаем bearer token после можем пользоваться всеми эндпоинтами

Перед тестом прошу ознакомиться с схемой маршрутов в файле scheme.png