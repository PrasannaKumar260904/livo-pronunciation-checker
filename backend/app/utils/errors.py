from typing import Any

from fastapi import HTTPException


def raise_api_error(
    status_code: int,
    code: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> None:
    detail: dict[str, Any] = {
        "code": code,
        "message": message,
    }

    if extra:
        detail.update(extra)

    raise HTTPException(status_code=status_code, detail=detail)
