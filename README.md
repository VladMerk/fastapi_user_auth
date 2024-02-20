# fastapi_user_auth
Простая авторизация пользователей с помощью токенов в `FastAPI`.

Создание токенов реализовано с помощью публичного и приватного ключей
Для создания ключе необходимо выполнить следующие команды в каталоге, в котором должны находиться сертификаты:

```shell
openssl genrsa -out jwt-private.pem 2048
```

```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```