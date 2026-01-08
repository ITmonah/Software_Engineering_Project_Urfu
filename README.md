# YOLO Object Detection (FastAPI)

Кратко: сервис на FastAPI для детекции объектов на изображениях с использованием локальных YOLO-моделей и хранением предпочитаемой версии модели в Redis per-IP.

---

## Начало работы ✅

Требования:

- Python 3.8+ (рекомендовано 3.10+)
- Redis (локально или в контейнере)

Установка зависимостей:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

```

Запуск Redis (например, в Docker):

```bash
docker run -p 6379:6379 --name redis -d redis:latest
```

Запуск сервера:

```bash
uvicorn main:app --reload
```

Документация API автоматически доступна:

- Swagger UI: `http://127.0.0.1:8000/docs`

---

## Краткая структура проекта 🔧

- `main.py` — точка входа, управляет жизненным циклом приложения (инициализация Redis)
- `api/model.py` — регистрация роутов API
- `api/endpoints/modelEnd.py` — реализация логики детекции и смены версии
- `modelsPyd.py` — pydantic-модели ответов API
- `redis_client/client.py` — клиент для Redis (async)
- `helpers/logger.py` — простая утилита логирования в консоль
- `tests/tests.py` — набор тестов для конечных точек
---

## Маршруты API (подробно) 🛣️

### 1) GET /detect

**Описание:** детектирует объекты на изображении по публичной ссылке. Выбор версии модели происходит на основе записи в Redis для IP клиента (ключ = IP адрес, значение = `"11s"` или `"11m"`). Если версия не задана — по умолчанию используется `11s`.

**Параметры:**

- `image_url` (query, string) — URL изображения

**Пример запроса (curl):**

```bash
curl "http://127.0.0.1:8000/detect?image_url=https://i.ytimg.com/vi/jg8ixdQzrjc/maxresdefault.jpg"
```

**Формат ответа:** (pydantic-модель `DetectionResponse`)

```json
{
  "results": [
    {
      "xmin": 235.77236938476562,
      "ymin": 0.0,
      "xmax": 1232.0889892578125,
      "ymax": 720.0,
      "confidence": 0.6995765566825867,
      "class_": 15,
      "name": "cat"
    }
  ]
}
```

**Примечания:**

> - IP клиента определяется из заголовков `X-Forwarded-For`, затем `X-Real-IP`, и в последнюю очередь из `request.client.host`.

---

### 2) GET /change_version

**Описание:** устанавливает предпочитаемую версию модели для текущего IP в Redis;

**Параметры:**

- `version` (query, int) — индекс в списке `available_version = ["11s", "11m"]` (0 → `11s`, 1 → `11m`)

**Пример запроса (curl):**

```bash
curl "http://127.0.0.1:8000/change_version?version=1"
```


**Формат ответа:** (pydantic-модель `ChangeModelResponse`)

```json
{ "result": "Версия модели изменена на 11m" }
```

---



## Тесты 🧪

Запустить тесты:

```bash
pytest tests/tests.py -q
```

Примечание: тест `test_detect_valid_image` делает реальный запрос по URL изображения и запускает модель — для этого требуется наличие `.pt` файлов и рабочий Redis; тесты могут быть долгими и зависят от окружения.


---

## Полезные команды (сводка) 📝

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск Redis в Docker
docker run -p 6379:6379 --name redis -d redis:latest

# Запуск сервера в режиме разработки
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Запуск тестов
pytest tests/tests.py -q
```
