from config import create_app, connexion_app, db
from users import users_blueprint
from trails import trails_blueprint
from feature import features_blueprint, trail_features_blueprint

# Creates the Flask app instance
app = create_app()

@app.route("/")
def home():
    return render_template("home.html")

# Registers each blueprint under a specific URL prefix
app.register_blueprint(users_blueprint, url_prefix="/api/users")
app.register_blueprint(trails_blueprint, url_prefix="/api/trails")
app.register_blueprint(features_blueprint, url_prefix="/api/features")
app.register_blueprint(trail_features_blueprint, url_prefix="/api/trail_features")

# Adds the OpenAPI specification so that Connexion can generate routes automatically
connexion_app.add_api(
    "static/swagger.yml",
    arguments={"title": "Trail Management API"},
    options={
        "swagger_ui": True,
        "swagger_ui_config": {"deepLinking": True},
        "swagger_ui_oauth_config": {"clientId": "your-client-id"},
    },
)

# Enters the app context to allow database operations
with app.app_context():
    db.create_all()  # Creates the database tables if they don't already exist

# Starts the server on port 5000 when this file is run directly
if __name__ == "__main__":
    connexion_app.run(port=8000)
