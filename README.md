# Python Backend

## Setup and Installation

This project requires Python 3.12 and uses Poetry for package management and dependency resolution. You can install the project using either **Conda + Poetry** or **Poetry only**.

### 1. Clone the Repository

```bash
git clone https://github.com/deniskirbaba/python-backend.git
cd python-backend
```

### 2. Installation Options

#### Conda + Poetry

Ensure you have Conda installed, then:

```bash
conda env create -f environment.yml
conda activate python-backend
poetry install
```

#### Poetry Only

Ensure you have Python 3.12 and Poetry installed, then:

```bash
poetry install
```

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

- Пример кода API на FastAPI: [fast_api_server.py](/lecture_1/learning-scripts/fast_api_server.py)

- Тесты для проверки: [test.py](/tests/test_math_api.py)

### Решение

#### Структура

```bash
└── lecture_1
   └── math_api
      ├── __init__.py
      ├── app.py            # ASGI application (main entry point)
      ├── routes.py         # Handlers and routes for the API
      ├── utils.py          # Validation and request body parsing
      └── services.py       # Factorial, Fibonacci, mean calculations
```

#### Запуск сервера

   Чтобы запустить сервер на `localhost:8000`, используйте следующую команду:

   ```bash
   uvicorn lecture_1.math_api.app:app --port 8000
   ```

#### Запуск тестов

```bash
poetry run pytest -vv --showlocals --strict ./tests/test_math_api.py
```
