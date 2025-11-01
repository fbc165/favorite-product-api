#!/bin/sh
echo "==== Applying database migrations ===="
alembic -c favorite_product_api/databases/postgresql/alembic.ini upgrade head

echo "\n==== Running application ===="
uvicorn favorite_product_api.app:app --host 0.0.0.0 --port 9900