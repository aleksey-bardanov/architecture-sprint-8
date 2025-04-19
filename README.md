# Sprint 8

## Как запустить

`docker compose up -d --build`

## Как проверить:

* [frontend](http://localhost:3000/)
* [backend/api](http://localhost:8000/docs)

### Ответы от бэкенда

* 401 - если попытаться отправить запрос без токена от Keycloak (например через /docs)
* 403 - если запрос отправит авторизованный пользователь, но без роли `prothetic_user`
* 200 - если запрос отправит авторизованный пользователь, c ролью `prothetic_user`