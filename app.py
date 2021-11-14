if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # before rts_lib import

    from flask import Flask
    from rts_lib import init_db

    app = Flask(__name__)
    db = init_db(app)

    with app.app_context():
        db.create_all()
