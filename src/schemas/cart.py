from pydantic import BaseModel


class CartProductUpdateScheme(BaseModel):
    amount: int | None = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}
