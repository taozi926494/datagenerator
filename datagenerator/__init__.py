from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datagenerator import config

app = Flask(__name__)
app.config.from_object(config)
cors = CORS(app, resources=r'/*', supports_credentials=True)
app.config['SECRET_KEY'] = 'secret!'
db = SQLAlchemy(app, session_options=dict(autocommit=False, autoflush=True))


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


from datagenerator.views import bp
app.register_blueprint(bp)


