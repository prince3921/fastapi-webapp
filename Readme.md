
## migration with alembic
```py
alembic init migrations
alembic revision --autogenerate -m "add user_id to blogs model"
alembic upgrade head
```

