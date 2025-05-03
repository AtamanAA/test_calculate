# [Stress calclulate](https://stress-calculate.herokuapp.com)
Проект для проведення проектувальних розрахунків на міцність силових елементів конструкції.
Доступні:
1. Розрахунок товщини стінки труби високого тиску
2. Розрахунок запасів міцності для різьбового з'єднання при осьовому навантажені



## Для локального розгортання проекту (команди для Windows)

1. Склонувати репозиторій
    ```bash    
    git clone https://github.com/AtamanAA/test_calculate.git
    ```
2. Встановити venv та активувати його
    ```bash
    python -m venv venv
   .\venv\Scripts\activate    
    ```
3. Інсталювати сторонні пакети у venv
    ```bash
    python -m pip install -r requirements.txt    
    ```
4. Виконати запуск основного web-серверу
    ```bash
    python manage.py runserver   
    ```
5. В браузері перейти на головну сторінку
    http://127.0.0.1:8000/


For autocomplete Sass files to style.css use FileWatcher in PyCharm
https://www.jetbrains.com/help/pycharm/transpiling-sass-less-and-scss-to-css.html