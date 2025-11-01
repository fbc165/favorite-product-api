from fastapi import FastAPI

from favorite_product_api.router import api_v1_router

app = FastAPI(
    title="Favorite Product API",
    description="API para gerenciamento dos produtos favoritos dos usuários",
    openapi_tags=[
        {
            "name": "Favorite products",
            "description": "Recursos relacionados aos produtos favoritos dos usuário",
        },
        {
            "name": "Clients",
            "description": "Recursos relacionados aos clientes",
        },
        {
            "name": "Authentication",
            "description": "Recursos relacionados à autenticação",
        },
    ],
)

app.include_router(api_v1_router, prefix="/api/v1")
