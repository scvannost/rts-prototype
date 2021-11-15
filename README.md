# rts-prototype

Ensure the following environment variables are defined before import:
- `POSTGRES_DATABASE`
- `POSTGRES_PASSWORD`
- `POSTGRES_URL`
- `POSTGRES_USER`

```python
import rts_lib
rts_db = rts_lib.init_db(app)
rts_lib.init_session(app, rts_db)
app.register_blueprint(rts_lib.blueprint, url_prefix="/<prefix>")
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
│   ├── models/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   └── users.py
│   └── pages/
│       ├── __init__.py
│       ├── core.py
│       └── templates/
│           ├── 401.html
│           ├── 403.html
│           ├── login.html
│           └── signup.html
└── tests/
```
