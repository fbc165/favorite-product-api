class NotFoundError(Exception):
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail

    def __str__(self):
        return self.detail


class EmailAlreadyExistsError(Exception):
    def __init__(self, detail: str = "Email address not available"):
        self.detail = detail

    def __str__(self):
        return self.detail


class ProductAlreadyIsFavoriteError(Exception):
    def __init__(self, detail: str = "Product already in user favorite product list"):
        self.detail = detail

    def __str__(self):
        return self.detail
