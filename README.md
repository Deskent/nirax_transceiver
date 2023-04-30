Ретранслятор запросов

# Info

    python3.10

    FastAPI==0.95.0

    Остальные зависимости смотрите в файле requirements.txt

## Работа с github

    Ветка main - используется для протестированной версии проекта. В нее мержим (merge) только
    когда убедились, что код не сломался и работает. На боевом сервере разворачиваем только из нее.

    Ветка dev - используется как общая ветка для разработчиков проекта. Из нее производится
    развертывание на тестовом сервере.

    Все разработчики работают в своих ветках, который созданы из dev или main (в зависимости от
    необходимой актуальности), потом делают pull request в dev, затем производится развертывание
    на тестовом сервере и тестирование. Если все прошло успешно - создается пулл-реквест в main,
    из которой уже производится развертывание на боевом сервере.

## Clone repository

Перейти в папку, в которой будет располагаться проект.

### SSH (рекомендуется)

##### Добавить свой публичный ssh ключ в настройках аккаунта github.
[https://docs.github.com/ru/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=windows](https://docs.github.com/ru/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?platform=windows)

    git clone git@github.com:Deskent/nirax_transceiver.git

### HTTPS (если лень добавлять ключ, но при каждом действии придется вводить логин и пароль от github)

    git clone https://github.com/Deskent/nirax_transceiver.git

## Start/rebuild in docker

Склонировать репозиторий (см выше)

Зайти в папку с ним

    cd nirax_transceiver

Выбрать нужную ветку

    git checkout dev
            or
    git checkout main

Запустить файл restart.sh

    . ./restart.sh

Либо командой

    docker-compose up -d --build
