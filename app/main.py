import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.palindrome import PalindromeInputError, check_palindrome

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("lab3")

app = FastAPI(
    title="ТРПО: лабораторная работа №3",
    version="1.0.0",
    description="Вариант 28 — проверка строки на палиндром.",
)


# ---------- единый формат ошибок ----------

def error_response(status: int, code: str, message: str, details: list | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"error": {"code": code, "message": message, "details": details or []}},
    )


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    details = []
    for err in exc.errors():
        loc = [str(p) for p in err.get("loc", ()) if p != "body"]
        details.append({"field": ".".join(loc) or "body", "message": err.get("msg", "")})
    log.info("VALIDATION_ERROR %s %s", request.url.path, details)
    return error_response(400, "VALIDATION_ERROR", "Переданные данные не прошли проверку", details)


@app.exception_handler(StarletteHTTPException)
async def http_handler(request: Request, exc: StarletteHTTPException):
    codes = {404: ("NOT_FOUND", "Ресурс не найден"), 405: ("METHOD_NOT_ALLOWED", "Метод не поддерживается")}
    code, message = codes.get(exc.status_code, ("HTTP_ERROR", str(exc.detail)))
    return error_response(exc.status_code, code, message)


@app.exception_handler(Exception)
async def internal_handler(request: Request, exc: Exception):
    log.exception("INTERNAL_ERROR")
    return error_response(500, "INTERNAL_ERROR", "Внутренняя ошибка сервера")


# ---------- вариант 28 ----------

class PalindromeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str


class PalindromeData(BaseModel):
    text: str
    normalized: str
    isPalindrome: bool
    message: str


class PalindromeResponse(BaseModel):
    data: PalindromeData


@app.post(
    "/api/v1/palindrome",
    response_model=PalindromeResponse,
    summary="Проверка строки на палиндром",
    tags=["Вариант 28"],
)
def palindrome(body: PalindromeRequest):
    try:
        result = check_palindrome(body.text)
    except PalindromeInputError as e:
        log.info("VALIDATION_ERROR text=%r: %s", body.text, e)
        return error_response(400, "VALIDATION_ERROR", "Переданные данные не прошли проверку",
                              [{"field": "text", "message": str(e)}])

    # вывод результата на экран сервера
    print(f"[palindrome] «{result.text}» — {result.message}", flush=True)

    return {
        "data": {
            "text": result.text,
            "normalized": result.normalized,
            "isPalindrome": result.is_palindrome,
            "message": result.message,
        }
    }
