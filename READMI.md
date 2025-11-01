# Для миграций
Создайте app.db  (если не создана в корне проека)
### Создаем миграцию
alembic revision --autogenerate -m "init new tables"

### Применяем 
alembic upgrade head

### Откатываем миграцию (если нужно)
alembic downgrade -1


# Локальный запуск 
## Создайте .venv и установити в него зависимости 
python3 -m venv .venv
pip install -r requirements.txt

## Активируйте .venv 
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate        # Windows

## Запустите 
uvicorn main:app --reload

перейдите по http://localhost:8000/docs#/



# Docker запуск 
## Запустите docker из корня и запустите build
docker build -t tz_app .
## Запустите контейнер:
docker run -d -p 8000:8000 tz_app


перейдите по http://localhost:8000/docs#/