# Codexchanger
## Товарищи, в папке frontend - мы пишем и создаем фронтенд сайта, в папке backend - бекенд сайта, а в папке mobile - мобильное приложение
# Зависимости:
## Backend:
```
pip install fastapi
pip install mysql-connector-python
pip install hypercorn
pip install uvicorn
```
## Для запуска серверного приложения (без перехода в папку backend) для тестирования:
```
python -m uvicorn backend.server:app --reload
```
## Для запуска серверного приложения (без перехода в папку backend) для релиза:
```
python -m hypercorn backend.server:app --bind [host]:80
```
## Вместо [host] указывается адрес. В случае нашего сервера - это: ```92.53.105.101```
