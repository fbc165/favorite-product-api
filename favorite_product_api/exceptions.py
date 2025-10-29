class NotFoundError(Exception):
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail

    def __str__(self):
        return self.detail
