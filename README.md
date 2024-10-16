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

### Task

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

### Solution

[math_api](/lecture_1/math_api/)

#### Structure

```bash
└── lecture_1
   └── math_api
      ├── __init__.py
      ├── app.py            # ASGI application (main entry point)
      ├── routes.py         # Handlers and routes for the API
      ├── utils.py          # Validation and request body parsing
      └── services.py       # Factorial, Fibonacci, mean calculations
```

#### Server startup

   Чтобы запустить сервер на `localhost:8000`, используйте следующую команду:

   ```bash
   cd python-backend
   uvicorn lecture_1.math_api.app:app --port 8000
   ```

#### Testing

```bash
cd python-backend
poetry run pytest -vv --showlocals --strict ./tests/test_math_api.py
```

## 2 - API

### Task

REST + RPC API for online shop

Ресурсы:

- корзина (cart)

    Пример структуры ресурса:

    ```json
    {
        "id": 123,  // идентификатор корзины
        "items": [  // список товаров в корзине
            {
                "id": 1, // id товара
                "name": "Туалетная бумага \"Поцелуй\", рулон", // название
                "quantity": 3, // количество товара в корзине
                "available": true // доступе ли (не удален ли) товар
            }, 
            {
                "id": 535, 
                "name": "Золотая цепочка \"Abendsonne\"", 
                "quantity": 1,
                "available": false,
            },
        ],
        "price": 234.4 // общая сумма заказа
    }
    ```

- товар (item)

    Пример структуры ресурса:

    ```json
    {
        "id": 321, // идентификатор товара
        "name": "Молоко \"Буреночка\" 1л.", // наименование товара
        "price": 159.99, // цена товара
        "deleted": false // удален ли товар, по умолчанию false
    }
    ```

Запросы для реализации:

- cart
  - `POST cart` - создание, работает как RPC, не принимает тело, возвращает
    идентификатор
  - `GET /cart/{id}` - получение корзины по `id`
  - `GET /cart` - получение списка корзин с query-параметрами
    - `offset` - неотрицательное целое число, смещение по списку (опционально,
      по-умолчанию 0)
    - `limit` - положительное целое число, ограничение на количество
      (опционально, по-умолчанию 10)
    - `min_price` - число с плавающей запятой, минимальная цена включительно
      (опционально, если нет, не учитывает в фильтре)
    - `max_price` - число с плавающей запятой, максимальная цена включительно
      (опционально, если нет, не учитывает в фильтре)
    - `min_quantity` - неотрицательное целое число, минимальное общее число
      товаров включительно (опционально, если нет, не учитывается в фильтре)
    - `max_quantity` - неотрицательное целое число, максимальное общее число
      товаров включительно (опционально, если нет, не учитывается в фильтре)
  - `POST /cart/{cart_id}/add/{item_id}` - добавление в корзину с `cart_id`
    предмета с `item_id`, если товар уже есть, то увеличивается его количество
- item
  - `POST /item` - добавление нового товара
  - `GET /item/{id}` - получение товара по `id`
  - `GET /item` - получение списка товаров с query-параметрами
    - `offset` - неотрицательное целое число, смещение по списку (опционально,
      по-умолчанию 0)
    - `limit` - положительное целое число, ограничение на количество
      (опционально, по-умолчанию 10)
    - `min_price` - число с плавающей запятой, минимальная цена (опционально,
      если нет, не учитывает в фильтре)
    - `max_price` - число с плавающей запятой, максимальная цена (опционально,
      если нет, не учитывает в фильтре)
    - `show_deleted` - булевая переменная, показывать ли удаленные товары (по
      умолчанию `False`)
  - `PUT /item/{id}` - замена товара по `id` (создание запрещено, только замена
    существующего)
  - `PATCH /item/{id}` - частичное обновление товара по `id` (разрешено менять
    все поля, кроме `deleted`)
  - `DELETE /item/{id}` - удаление товара по `id` (товар помечается как
    удаленный)

### Solution

[online_shop](/lecture_2/online_shop/)

#### Structure

```bash
lecture_2
 └── online_shop
     ├── api
     │   ├── __init__.py
     │   ├── online_shop
     │   │   ├── __init__.py
     │   │   ├── contracts.py
     │   │   └── routes.py
     ├── __init__.py
     ├── main.py
     └── store
        ├── __init__.py
        ├── models.py
        └── queries.py
```

#### Server startup

```bash
cd python-backend
poetry run fastapi run ./lecture_2/online_shop/main.py
```

#### Testing

```bash
cd python-backend
poetry run pytest -vv --showlocals --strict ./tests/test_online_shop_api.py
```

## 3 - Docker & Monitoring

### Task

Integrate Docker with Prometheus and Grafana into any previously developed service (I chose the [online-shop](/lecture_2/online_shop/) service from HW-2).

### Solution

#### Structure

```bash
└── lecture_3
    └── hw3
        ├── docker
        │   └── online_shop
        │       └── Dockerfile
        ├── docker-compose.yml
        ├── grafana_dashboard
        │   └── grafana_dashboard.json
        ├── online_shop_api_ddoser.py
        ├── requirements.txt
        └── settings
            └── prometheus
                └── prometheus.yml
```

#### Startup

To run the services, Docker is required. Build the services using Docker Compose:

```bash
cd python-backend/lecture_3/hw3
docker compose build
```

Now, to start the services, run:

```bash
docker compose up -d
```

The online shop API service will be available at `http://0.0.0.0:8080` (`http://0.0.0.0:8080/docs` for Swagger documentation). To collect metrics, `prometheus-fastapi-instrumentator` has been integrated. Metrics can be accessed at `http://0.0.0.0:8080/metrics`.

Prometheus will be available at: `http://localhost:9090`.

Grafana will be available at: `http://0.0.0.0:3000`. The dashboard for monitoring can be imported from: [grafana_dashboard.json](/lecture_3/hw3/grafana_dashboard/grafana_dashboard.json).

![Dashboard Example 1](/lecture_3/hw3/grafana_dashboard/dashboard_example_1.png)

![Dashboard Example 2](/lecture_3/hw3/grafana_dashboard/dashboard_example_2.png)

To stop the services, run:

```bash
docker compose down
```

## 4 - Quality Assurance

### Task 1

Нужно расписать тесты для [demo_service](./lecture_4/demo_service/) из лекции 4. Сдача на основе процента
покрытия кода тестами - требуется добиться 100% покрытия. Тесты для сервиса должны лежать в этой директории (`tests/lecture_4/hw`).  
Команда, для запуска тестов:

```sh
poetry run pytest \
    -vv \
    --cov=lecture_4/demo_service \
    ./tests/lecture_4/hw
```

### Task 2

Реализовать скрипт для нагрузочного тестирования приложения. Длительность не менее 10 минут (а лучше больше), требуется
приложить в PR графики из Grafana с RPS и Success Rate (% успешных, то есть
200-х запросов), а так же отчет формируемый инструментом, если таковой есть.
