# ТРПО — лабораторная работа №3

Вариант 28: клиент отправляет серверу строку, сервер проверяет, является ли она палиндромом
(пробелы, знаки препинания и регистр не учитываются), и возвращает результат клиенту.

Endpoint: `POST /api/v1/palindrome`. Стек: Python 3.12+, FastAPI, Uvicorn.

## Запуск (Git Bash, Windows)

```bash
python -m venv .venv
source .venv/Scripts/activate        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Сервер: http://127.0.0.1:8000, документация Swagger: http://127.0.0.1:8000/docs

## Проверка

Консольный клиент (во втором терминале, с активированным окружением):

```bash
winpty python client.py     # в Git Bash; в PowerShell или терминале IDE — просто python client.py
```

Через curl:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/palindrome \
  -H "Content-Type: application/json" \
  -d '{"text": "А роза упала на лапу Азора"}'
```

Ответ:

```json
{"data": {"text": "А роза упала на лапу Азора", "normalized": "арозаупаланалапуазора", "isPalindrome": true, "message": "является палиндромом"}}
```

Тесты:

```bash
pytest -q
```

## Правила проверки

- пробелы, знаки препинания и регистр не учитываются, «ё» = «е»;
- строка обязательна, тип — string, длина до 1000 символов;
- в строке должна быть хотя бы одна буква или цифра.

Ошибки возвращаются в едином формате `{"error": {"code", "message", "details"}}` с кодом `400 VALIDATION_ERROR`.
