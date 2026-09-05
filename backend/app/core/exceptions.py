from fastapi import HTTPException
class AppError(HTTPException):
    def __init__(self, detail: str, status_code: int = 400): super().__init__(status_code, detail)
class NotFoundError(AppError):
    def __init__(self, detail="Resource not found"): super().__init__(detail, 404)
