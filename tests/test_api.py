from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
URL = "/api/v1/palindrome"


def test_ok_palindrome():
    r = client.post(URL, json={"text": "А роза упала на лапу Азора"})
    assert r.status_code == 200
    assert r.json()["data"]["isPalindrome"] is True
    assert r.json()["data"]["message"] == "является палиндромом"


def test_ok_not_palindrome():
    r = client.post(URL, json={"text": "Привет"})
    assert r.status_code == 200
    assert r.json()["data"]["isPalindrome"] is False


def check_validation(r, field="text"):
    assert r.status_code == 400
    err = r.json()["error"]
    assert err["code"] == "VALIDATION_ERROR"
    assert any(d["field"] == field for d in err["details"])


def test_empty_string():
    check_validation(client.post(URL, json={"text": "   "}))


def test_no_letters():
    check_validation(client.post(URL, json={"text": "?!.,"}))


def test_too_long():
    check_validation(client.post(URL, json={"text": "a" * 1001}))


def test_missing_field():
    check_validation(client.post(URL, json={}))


def test_wrong_type():
    check_validation(client.post(URL, json={"text": 12321}))
    check_validation(client.post(URL, json={"text": None}))


def test_extra_field():
    check_validation(client.post(URL, json={"text": "Шалаш", "lang": "ru"}), field="lang")


def test_invalid_json():
    r = client.post(URL, content=b"{text: ", headers={"Content-Type": "application/json"})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"


def test_wrong_method():
    r = client.get(URL)
    assert r.status_code == 405
    assert r.json()["error"]["code"] == "METHOD_NOT_ALLOWED"
