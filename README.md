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

- Пример кода API на FastAPI: [fast_api_server.py](/learning/week1/fast_api_server.py)

- Тесты для проверки: [test_hw_1.py](/tests/test_hw_1.py)

### Решение

#### Структура

```bash
├── pyproject.toml
├── src
│   ├── math_api
│   │   ├── app.py            # ASGI application (main entry point)
│   │   ├── routes.py         # Handlers and routes for the API
│   │   ├── utils.py          # Validation and request body parsing
│   │   ├── services.py       # Factorial, Fibonacci, mean calculations
│   │   └── __init__.py       # For making Python package

│   └── python_backend.egg-info
└── tests
    ├── __init__.py
    └── test_hw1.py
```

#### Инструкции по установке и запуску

1. **Клонирование репозитория**

   Для начала клонируйте репозиторий и перейдите в директорию проекта:

   ```bash
   git clone https://github.com/deniskirbaba/python-backend.git
   cd python-backend
   ```

1. **Установка зависимостей и сборка**

   Для запуска требуется `python` версии выше `3.12`.
   Все остальные необходимые зависимости и инструкции по сборке определены в файле `pyproject.toml`. В качестве ASGI-сервера используется `uvicorn`. Для установки модуля и его зависимостей выполните следующую команду:

   ```bash
   pip install .
   ```

1. **Запуск сервера**

   Чтобы запустить сервер на `localhost:8000`, используйте следующую команду:

   ```bash
   start-math-server
   ```

   Эта команда запустит сервер, используя скрипт, описанный в файле `pyproject.toml`.
