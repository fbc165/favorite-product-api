#!/bin/sh

echo "\n==== Running application ===="
uvicorn favorite_product_api.app:app --host 0.0.0.0 --port 9900