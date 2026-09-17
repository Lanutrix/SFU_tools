# LMS SFU

Клиент и утилиты для Modeus (расписание / люди) и LMS SFU (отметка посещаемости).

## Структура

```
lms_sfu/
  config.py          # env: TOKEN, ATTENDEE_PERSON_ID, MOODLE_SESSION
  models/            # Event, Person
  parsers/           # разбор ответов API
  modeus/            # HTTP-клиент и методы Modeus
  moodle/            # отметка на LMS
examples/
  demo.py            # локальные примеры
```

## Установка

```bash
pip install -r requirements.txt
cp .env.example .env
```

Заполни `.env`:

```
ATTENDEE_PERSON_ID=
TOKEN=
MOODLE_SESSION=
```

## Примеры

```bash
python -m examples.demo schedule
python -m examples.demo people
python -m examples.demo attendance
python -m examples.demo attendance "https://lms.sfedu.ru/mod/attendance/attendance.php?qrpass=...&sessid=..."
```

## Использование в коде

```python
from lms_sfu.modeus import get_schedule, search_people
from lms_sfu.moodle import mark_lesson

events = get_schedule("2026-09-13", "2026-09-20")
people = search_people(name="Иван", year=2024, specialty="системы")
```
