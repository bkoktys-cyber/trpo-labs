"""Консольный клиент для ЛР3 (вариант 28).

Запуск:  python client.py                       (сервер на http://127.0.0.1:8000)
         python client.py --url http://host:port
Пустая строка или Ctrl+C — выход.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request


def send(url: str, text: str) -> tuple[int, dict]:
    body = json.dumps({"text": text}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{url}/api/v1/palindrome",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as e:
        return e.code, json.load(e)


def main() -> None:
    parser = argparse.ArgumentParser(description="Проверка палиндрома через сервер")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    while True:
        try:
            text = input("Введите строку (пустая — выход): ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text == "":
            break
        try:
            status, payload = send(args.url, text)
        except urllib.error.URLError as e:
            print(f"Сервер недоступен: {e.reason}")
            continue

        if status == 200:
            print(f"Ответ сервера: «{payload['data']['text']}» — {payload['data']['message']}")
        else:
            err = payload.get("error", {})
            reasons = "; ".join(d["message"] for d in err.get("details", [])) or err.get("message", "")
            print(f"Ошибка {status} {err.get('code')}: {reasons}")


if __name__ == "__main__":
    main()
