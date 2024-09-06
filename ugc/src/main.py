import sentry_sdk
from flask import Flask
from flask_jwt_extended import JWTManager

from api.v1.bookmarks import bp as bookmarks_bp
from api.v1.events import bp as events_bp
from api.v1.likes import bp as likes_bp
from api.v1.reviews import bp as reviews_bp
from core.config import settings

app = Flask(__name__)
app.config.from_object(settings)

# Setup jwt authorization
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = settings.auth.JWT_SECRET_KEY

app.config['MONGO_URI'] = settings.mongo.URI

sentry_sdk.init(
    dsn=settings.sentry.URL,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


app.register_blueprint(events_bp, url_prefix='/eventapi/v1')
app.register_blueprint(bookmarks_bp, url_prefix='/eventapi/v1/bookmarks')
app.register_blueprint(likes_bp, url_prefix='/eventapi/v1/likes')
app.register_blueprint(reviews_bp, url_prefix='/eventapi/v1/reviews')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=settings.FLASK_PORT,
        debug=settings.FLASK_DEBUG,
    )
