# Python Backend

## 1 - Основы сети и Python Backend

### Задача

Реализовать "Математическое API" через ASGI-совместимую функцию. Требования:

- Запросы без обработчиков (не тот метод, не тот путь) должны возвращать ошибку `404 Not Found`.

- Запрос `GET /factorial` (факториал числа `n`):

  - Возвращает результат в теле ответа в формате JSON: `{"result": 123}`.
  - В запросе должен быть query-параметр `n: int`.
  - Если параметра нет или он не является числом — возвращается ошибка `422 Unprocessable Entity`.
  - Если параметр меньше 0 — возвращается ошибка `400 Bad Request`.

- Запрос `GET /fibonacci/{n}` (n-ое число Фибоначчи):

  - Возвращает результат в теле ответа в формате JSON: `{"result": 123}`.
  - В запросе должен быть path-параметр `n: int`.
  - Если параметр не указан или не является числом — ошибка `422 Unprocessable Entity`.
  - Если параметр меньше 0 — ошибка `400 Bad Request`.

- Запрос `GET /mean` (среднее арифметическое массива):

  - Возвращает результат в теле ответа в формате JSON: `{"result": 123}`.
  - В теле запроса должен быть непустой массив `float`-значений (например, `[1, 2.3, 3.6]`).
  - Если тело запроса не является массивом `float` — ошибка `422 Unprocessable Entity`.
  - Если массив пустой — ошибка `400 Bad Request`.

- [Спецификация ASGI](https://asgi.readthedocs.io/en/latest/specs/www.html#http)

- Пример кода API на FastAPI: [fast_api_server.py](/01_network/learning-scripts/fast_api_server.py)

- Тесты для проверки: [test.py](/01_network/tests/test.py)

### Решение

#### Структура

```bash
└── 01_network
    ├── math-api
    │   ├── __init__.py
    │   ├── app.py            # ASGI application (main entry point)
    │   ├── routes.py         # Handlers and routes for the API
    │   ├── utils.py          # Validation and request body parsing
    │   ├── services.py       # Factorial, Fibonacci, mean calculations
    ├── tests
    |   ├── __init__.py
    |   └── test.py
    └── requirements.txt

```

#### Инструкции по установке и запуску

1. **Клонирование репозитория**

   Для начала клонируйте репозиторий и перейдите в директорию проекта:

   ```bash
   git clone https://github.com/deniskirbaba/python-backend.git
   cd python-backend/01_network
   ```

2. **Установка зависимостей**

    Зависимости прописаны в [requirements.txt](/01_network/requirements.txt).  
   Для запуска требуется `python` версии выше `3.12`.  
   В качестве ASGI-сервера используется `uvicorn`. Для установки зависимостей выполните следующую команду:

   ```bash
   pip install -r requirements.txt
   ```

3. **Запуск сервера**

   Чтобы запустить сервер на `localhost:8000`, используйте следующую команду:

   ```bash
   uvicorn math-api.app:app --port 8000
   ```

4. **Запуск тестов**

    Для запусков тестов отройте новый терминал, перейдите в папку репозитория `/python-backend/01_network` и выполните:

    ```bash
    pytest tests/test.py
    ```