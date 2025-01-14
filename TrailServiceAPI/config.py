from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from connexion import App
from urllib.parse import quote_plus

# Creates instances of SQLAlchemy and Marshmallow for database and schema handling
db = SQLAlchemy()
ma = Marshmallow()

# Establishes the Connexion application to manage the API
connexion_app = App(__name__, specification_dir="./")

def create_app():
    # Retrieves the underlying Flask app from the Connexion app
    app = connexion_app.app
    # Enables Cross-Origin Resource Sharing
    CORS(app)

    # Sets parameters for the SQL Server connection
    db_params = {
        "DRIVER": "ODBC Driver 17 for SQL Server",
        "SERVER": "dist-6-505.uopnet.plymouth.ac.uk",
        "DATABASE": "COMP2001_JGoulding",
        "UID": "JGoulding",
        "PWD": "XtwY858+",
        "TrustServerCertificate": "yes",
        "Encrypt": "yes",
    }

    # Builds the connection string from the parameters
    connection_string = ";".join([f"{k}={quote_plus(v)}" for k, v in db_params.items()])
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initializes SQLAlchemy and Marshmallow with the Flask app
    db.init_app(app)
    ma.init_app(app)

    return app
