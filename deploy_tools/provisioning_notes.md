Обеспеченияработы нового сайта
===============================
## Необходимые файлы:
* nginx
* Python => 3.8
* virtualenv + pip
* Git

пример в UBUNTU:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python3.8 python3.8-venv


* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domain.com


## Служба Systemd

* см. ginicorn-systemd.template.service
* заменить SITENAME на нужное имя

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username
/home/username
      └── sites
          └── SITENAME
              ├── database
              ├── source
              ├── static
              └── virtualenv





