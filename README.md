Выбор полезного содержимого страницы со статьёй сайта
-----------------------------------------------------

Перейдите туда, где будет находиться ваш проект

```cd ~```

Клонируем репозиторий https://github.com/protasovse/tenzor_parser

```git clone https://github.com/protasovse/tenzor_parser.git```


Виртуальная среда
-----------------

Если у вас нет virtualenv, вам нужно его установить. Это позволит вам иметь отдельные
установки программного обеспечения для каждого проекта:

```sudo pip install virtualenv```

Теперь начнём:

```
cd tenzor_parser
virtualenv venv
source venv/bin/activate
```

Теперь установите все, что нам нужно:

```pip install -r requirements.txt```

И проверить, что у нас есть Django:

```python -c "import django; print(django.get_version())"```

Теперь через командную строку добавим URL страницы, с которой нужно взять полезное содержимое:

```python manage.py parse -u https://lenta.ru/news/2018/12/25/podarochek/```




