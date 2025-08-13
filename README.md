# unboil-sqlalchemy-utils

Async pagination for SQLAlchemy (async) queries.

## Example

```python
from sqlalchemy import select
from unboil_sqlalchemy_utils import paginate, count, fetch_all, fetch_one

# Paginate results for a model
result = await paginate(
    session=my_async_session,
    statement=select(MyModel),
    offset=0,   # start index
    limit=10    # page size
)
print(result.items)         # List of items for this page
print(result.total)         # Total number of items
print(result.total_pages)   # Total number of pages
print(result.current_page)  # Current page (1-based)
print(result.has_more)      # True if more results exist

# Fetch all results (no pagination)
all_items = await fetch_all(my_async_session, select(MyModel))

# Fetch a single result
one_item = await fetch_one(my_async_session, select(MyModel).where(MyModel.id == 1))

# Count total rows for a query
total = await count(my_async_session, select(MyModel))
```

---
MIT License