# 1c_applications-back
synch with 1C


API DOC: http://91.201.214.221/api/v1/swagger/
ADMIN : http://91.201.214.221/admin/
USER : admin_user
PASSWORD : 123

## Запуск проекта

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/<username>/rus-1c_applications-back.git
    ```

2. Перейдите в каталог проекта:

    ```bash
    cd 1c_applications-back/
    ```
    не забудьте проверить что файл .env существует
     ```bash
    cp .env.example .env
    ```

3. Запустите проект с помощью Docker Compose:

    ```bash
    docker compose up -d
    ```

4. Подключитесь к контейнеру:

    ```bash
    docker exec -it 1c_applications-back-main-1 sh
    ```

5. Выполните миграции базы данных:

    ```bash
    python manage.py migrate
    ```

6. Соберите статические файлы:

    ```bash
    python manage.py collectstatic
    ```

7. Создайте суперпользователя:

    ```bash
    python manage.py createsuperuser
    ```

## Обновления проекта

1. Перейдите в каталог проекта:

    ```bash
    cd 1c_applications-back/
    ```

2. Обновите репозиторий:

    ```bash
    git pull
    ```

3. Перезапустите Docker Compose:

    ```bash
    docker compose restart
    ```

4. Если есть миграции, выполните их:

    ```bash
    docker exec -it 1c_applications-back-main-1 sh
    python manage.py migrate
    ```

5. Если нужно обновить статические файлы, выполните:

    ```bash
    rm -rf static/static_root/
    python manage.py collectstatic
    ```
