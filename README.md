# rts-prototype

Ensure the following environment variables are defined before import:
- `POSTGRES_DATABASE`
- `POSTGRES_PASSWORD`
- `POSTGRES_URL`
- `POSTGRES_USER`

```python
from rts_lib import db, SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app: Flask)
```

## First-time set up

Run `python app.py` or equivalent to generate tables via `db.create_all()`.

# File Structure
```
rts-prototype/
├── LICENSE
├── pyproject.toml
├── README.md
├── reqirements.dev.txt
├── reqirements.txt
├── setup.cfg
│
├── app.py
├── rts_lib/
│   ├── __init__.py
│   └── models/
│       ├── __init__.py
│       └── core.py
└── tests/
```
