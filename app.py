from dotenv import load_dotenv
load_dotenv() # before rts_lib import

from flask import Flask
import rts_lib

app = Flask(__name__)
db = rts_lib.init_db(app)
rts_lib.init_session(app, db)
app.register_blueprint(rts_lib.blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
