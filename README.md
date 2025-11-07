# WeatherAPI

Сервис на FastAPI, который подтягивает актуальную погоду из OpenWeather (по координатам или названию города), нормализует ответ и сохраняет историю запросов в PostgreSQL для последующей аналитики.

## Возможности
- Получение погоды по `city` или паре `lat/lon` с автоматическим приоритетом координат.
- Синхронизация с OpenWeather через асинхронный `httpx` и кеширование базовых параметров.
- Сохранение истории обращений в таблицу `weather_requests` (SQLAlchemy + Alembic миграции).
- REST API с автогенерируемой документацией (`/docs`, `/redoc`) и включённым CORS.
- Готовый Docker Compose (FastAPI + PostgreSQL) и автозапуск миграций при старте backend.

## Технологический стек
- FastAPI, Pydantic, uvicorn
- httpx
- PostgreSQL 14, SQLAlchemy 2.0, asyncpg, Alembic
- Docker / Docker Compose
- loguru

## Структура проекта
```
WeatherAPI
├── docker-compose.yaml
├── README.md
├── tests.ipynb
└── src
    ├── main.py                # FastAPI приложение + регистрация роутов и middleware
    ├── apps/get_weather.py    # HTTP endpoints
    ├── services/weather.py    # Клиент OpenWeather
    ├── database/              # Конфигурация, ORM, core-слой и worker
    ├── templates/schemas/     # Pydantic-схемы ответов
    ├── migrations/            # Alembic миграции
    ├── requirements.txt
    └── Dockerfile
```

## Переменные окружения
Создайте файл `.env` в корне или прокиньте переменные в систему/CI.

| Переменная | Назначение |
| ---------- | ---------- |
| `OPEN_WEATHER_KEY` | API-ключ OpenWeather (https://openweathermap.org/api). |
| `DATABASE_HOST` | Хост PostgreSQL (для Docker укажите `db`). |
| `DATABASE_PORT` | Порт PostgreSQL (по умолчанию `5432`). |
| `DATABASE_NAME` | Имя базы (например, `weather`). |
| `DATABASE_LOGIN` | Пользователь PostgreSQL. |
| `DATABASE_PASSWORD` | Пароль PostgreSQL. |
| `DB_PORT` | Порт, проброшенный наружу для контейнера БД (используется в docker-compose). |
| `BACKEND_PORT` | Порт публикации FastAPI сервиса (например, `8000`). |

Пример `.env`:
```dotenv
OPEN_WEATHER_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=weather
DATABASE_LOGIN=postgres
DATABASE_PASSWORD=postgres
DB_PORT=5432
BACKEND_PORT=7655
```

## Быстрый старт (Docker)
1. Скопируйте репозиторий и перейдите в папку проекта.
2. Создайте `.env` по примеру выше.
3. Запустите инфраструктуру:
   ```bash
   docker compose up --build
   ```
4. Backend станет доступен на `http://localhost:${BACKEND_PORT}`. Документация по умолчанию доступна на `http://localhost:${BACKEND_PORT}/docs`.

Миграции (`alembic upgrade head`) выполняются автоматически при старте контейнера backend благодаря `lifespan`-хуку в `src/main.py`.

## API
### GET `/weather`
- **Параметры query**:
  - `city`: str, название города.
  - `lat`: float, широта (−90…90).
  - `lon`: float, долгота (−180…180).
- Нужно указать `city` *или* пару `lat`+`lon`. Если переданы оба варианта, используются координаты.

- **Ответ на запрос**:
  - `temperature`: float, температура в Цельсиях.
  - `wind_speed`: float, скорость ветра в м/с.
  - `weather_main`: str, обшая характеристика погоды.
- Нужно указать `city` *или* пару `lat`+`lon`. Если переданы оба варианта, используются координаты.

Пример запроса:
```bash
curl -G "http://localhost:{your_port}/weather" \
     --data-urlencode "city=Moscow"
```

Ответ:
```json
{
  "temperature": -5.32,
  "wind_speed": 4.12,
  "weather_main": "Snow"
}
```

Больше примеров в ноутбуке ```test.ipynb```

Ошибки:
- `400` — не переданы обязательные параметры.
- `500` — ошибка внешнего сервиса или базы (подробности в логах).


