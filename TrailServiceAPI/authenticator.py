import requests
import jwt
from flask import request, abort
from datetime import datetime, timedelta, timezone
from connexion.exceptions import OAuthProblem

# External authentication URL for validating user credentials
AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
# Secret key for encoding and decoding JWT tokens
SECRET_KEY = "DEFINITELY_NOT_YOUR_SECRET_KEY"


def authenticate():
    """
    Authenticate a user with the external API and return a JWT token.
    """
    body = request.get_json()
    # Checks if the request contains both email and password
    if not body or not body.get("email") or not body.get("password"):
        abort(400, "Email and password are required.")
    
    # Packages the credentials to send to the external service
    credentials = {
        "email": body["email"],
        "password": body["password"]
    }

    # Attempts to authenticate via the external API
    try:
        response = requests.post(AUTH_URL, json=credentials)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Returns an error if there's a problem making the request
        abort(500, f"Failed to authenticate: {e}")

    # Checks for a successful response and inspects the API's result
    if response.status_code == 200:
        try:
            response_data = response.json()
            # The second element is expected to be "True" if the user is valid
            if len(response_data) > 1 and response_data[1] == "True":
                # Sets an expiration time for the token (one hour from the current time)
                expiration = datetime.now(timezone.utc) + timedelta(hours=1)
                payload = {
                    "email": body["email"],
                    "exp": expiration,
                    "role": "ADMIN"
                }
                # Creates the JWT token using the secret key
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                return {"token": token}, 200
            else:
                # Indicates invalid credentials if the API response is "False"
                abort(401, "Invalid credentials")
        except Exception as e:
            abort(500, f"Error processing response: {e}")
    else:
        abort(401, "Invalid credentials")


def validate_token(token, required_scopes=None):
    """
    Connexion-style token validation function.
    Connexion passes the JWT token string here (not a request object).
    """
    # Returns an error if no token is provided
    if not token:
        raise OAuthProblem(description="No token provided")

    try:
        # Decodes the token using the secret key
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        # Raises an error if the token has expired
        raise OAuthProblem(description="Token has expired.")
    except jwt.InvalidTokenError:
        # Handles other invalid token scenarios (e.g., tampering)
        raise OAuthProblem(description="Invalid token.")
