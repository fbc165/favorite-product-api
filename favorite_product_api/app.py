from fastapi import FastAPI


app = FastAPI(
    title="Favorite Product API",
    description="API para gerenciamento dos produtos favoritos dos usuários",
    openapi_tags=[
        {
            "name": "Favorite products",
            "description": "Recursos relacionados aos produtos favoritos dos usuário",
        },
        {
            "name": "Users",
            "description": "Recursos relacionados aos usuários",
        },
    ],
)
