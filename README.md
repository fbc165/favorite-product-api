# Favorite Product API

API para gerenciamento de produtos favoritos de usuários.

## Requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:

-   **Docker**: [Instruções de Instalação](https://docs.docker.com/get-docker/)
-   **Docker Compose**: [Instruções de Instalação](https://docs.docker.com/compose/install/)

## Configuração do Ambiente

1.  **Clone o Repositório**

    ```bash
    git clone https://github.com/fbc165/favorite-product-api.git
    cd favorite-product-api
    ```

2.  **Crie o Arquivo de Ambiente (`.env`)**

    Crie um arquivo chamado `.env` na raiz do projeto. Este arquivo é essencial para configurar as variáveis de ambiente da aplicação e do banco de dados.

    Copie e cole o conteúdo abaixo no seu arquivo `.env`:

    ```env
    SECRET_KEY=05GLXyRorXqfsDBcrsqtAbivb9c2tZmclT4XGqPEX0A=
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    POSTGRES_USER=aiqfome
    POSTGRES_PASSWORD=iqui1234
    POSTGRES_DB=aiqfome
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    PRODUCT_API_URL=https://fakestoreapi.com/products/
    ```

## Executando a Aplicação

Com o Docker e o Docker Compose instalados e o arquivo `.env` configurado, você pode iniciar a aplicação com um único comando:

```bash
docker-compose up --build
```

-   O comando `--build` força a reconstrução das imagens Docker, garantindo que quaisquer alterações no `Dockerfile` ou no código sejam aplicadas.
-   A API estará disponível em: `http://localhost:9900`
-   A documentação interativa (Swagger UI) estará em: `http://localhost:9900/docs`

## Como Testar a API

Você pode usar a documentação interativa do Swagger UI para testar todos os endpoints.

### 1. Crie um Usuário

-   Vá para a seção **Users**.
-   Abra o endpoint `POST /api/v1/users/`.
-   Clique em "Try it out".
-   Preencha o corpo da requisição com um nome, email e senha.
    ```json
    {
      "name": "Test User",
      "email": "test@example.com",
      "password": "password123"
    }
    ```
-   Clique em "Execute". Você deve receber uma resposta `200 OK` com os dados do usuário criado.

### 2. Faça Login para Obter um Token

-   Vá para a seção Authentication.
-   Abra o endpoint `POST /api/v1/auth/token`.
-   Clique em "Try it out".
-   Preencha o corpo da requisição com o email (`username`) e a senha (`password`) do usuário que você acabou de criar.
-   Clique em "Execute". Você receberá uma resposta com um `access_token`.
- A resposta da criação do usuário retornará um `uuid`. Copie este valor, pois ele será necessário para testar os endpoints de produtos favoritos (ex: `/api/v1/users/{user_uuid}/favorite-products/`).

### 3. Autorize suas Requisições

-   No topo da página do Swagger, clique no botão Authorize.
-   Na janela que abrir, cole o `access_token` que você recebeu no campo "Value".
    ```
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
    ```
-   Clique em "Authorize" e depois em "Close". Agora, todas as suas requisições feitas pelo Swagger incluirão o token de autenticação no formato correto.

### 4. Teste os Endpoints Protegidos

Agora você pode testar os endpoints que exigem autenticação, como adicionar ou listar produtos favoritos.

#### Adicionar um Produto Favorito

-   Vá para a seção Favorite products.
-   Abra o endpoint `POST /api/v1/users/{user_uuid}/favorite-products/`.
-   Clique em "Try it out".
-   Informe o `user_uuid` que você guardou no passo 1.
-   Informe o `product_id` de um produto que você deseja favoritar no corpo da requisição.
    ```json
    {
      "id": 1
    }
    ```
-   Clique em "Execute".

#### Listar Produtos Favoritos

-   Vá para a seção **Favorite products**.
-   Abra o endpoint `GET /api/v1/users/{user_uuid}/favorite-products/`.
-   Clique em "Try it out".
-   Informe o `user_uuid` que você guardou no passo 1.
-   Clique em "Execute". A resposta deve listar os produtos que você favoritou.

#### Remover produto favorito

-   Vá para a seção Favorite products.
-   Abra o endpoint `DELETE /api/v1/users/{user_uuid}/favorite-products/`.
-   Clique em "Try it out".
-   Informe o `user_uuid` que você guardou no passo 1.
-   Informe o `product_id` de um produto que você deseja favoritar.
-   Clique em "Execute".

## Escolhas que fiz para a construção da API
- Python com FastAPI para performance assíncrona devido ao I/O com a API de products. Além disso, ao usar usá-lo com o uvicorn, instâncias são reaproveitadas para atenderem outras requisições enquanto esperam por operações de I/O, diminuindo a necessidade de criação de várias instâncias e aumentando a escalabilidade
- Uso do driver psycopg v3 (em C) para melhor performance assíncrona com o banco de dados PostgreSQL
- Chamadas HTTP assíncronas para a API de produtos para diminuir o tempo de resposta ao fazer múltiplas chamadas
- Uso da imagem **slim** (imagem menor) do python para economizar recursos da máquina, aumentando a capacidade de escalabilidade
- Uso do pydantic v2 para validação robusta e velocidade por ser escrito em Rust
- Uso de UUID para aumentar a segurança das informações que expostas
