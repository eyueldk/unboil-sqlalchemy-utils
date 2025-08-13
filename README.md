# unboil-sqlalchemy-mixins

Reusable mixins for SQLAlchemy models, designed to save you time and reduce boilerplate in your Python ORM code.

## Features

- **IdentifiableMixin**: Adds a string primary key with optional prefix to your models.
- **TimestampedMixin**: Adds `created_at` and `updated_at` fields with automatic timestamping.

## Installation

```bash
pip install unboil-sqlalchemy-mixins
```

## Usage

### IdentifiableMixin

Add a string `id` primary key to your models. You can also use a prefix for the ID:

```python
from sqlalchemy.orm import DeclarativeBase
from unboil_sqlalchemy_mixins import IdentifiableMixin

class Base(DeclarativeBase):
    pass

class User(IdentifiableMixin, Base):
    __tablename__ = "users"
    # ... your fields ...

# Or with a prefix:
class PrefixedUser(IdentifiableMixin.with_prefix("user_"), Base):
    __tablename__ = "prefixed_users"
    # ... your fields ...
```

### TimestampedMixin

Add `created_at` and `updated_at` fields that are automatically managed:

```python
from sqlalchemy.orm import DeclarativeBase
from unboil_sqlalchemy_mixins import TimestampedMixin

class Base(DeclarativeBase):
    pass

class Post(TimestampedMixin, Base):
    __tablename__ = "posts"
    # ... your fields ...
```

## Mixins API

### IdentifiableMixin
- Adds a string `id` primary key (32 hex chars by default).
- Use `IdentifiableMixin.with_prefix(prefix)` to add a custom prefix to the ID.

### TimestampedMixin
- Adds `created_at` and `updated_at` fields (timezone-aware, auto-managed).

## License

MIT