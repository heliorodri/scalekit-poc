from flask import Flask, request, jsonify
from scalekit_backend.db.models import UserCredentials
from scalekit_backend.db import init_app as db_init_app
from scalekit_backend.users.user_credential_repository import UserCredentialRepository
from scalekit_backend.client.scalekit_client import ScClient
import os

app = Flask(__name__)

scalekit = ScClient()
user_service = UserCredentialRepository()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_init_app(app)


@app.route("/api/login")
def login():
    code = "random_string_123"
    return scalekit.authorization_url(code)


@app.route("/api/callback")
def callback():
    code = request.args.get("code") or ""
    error = request.args.get("error") or ""
    error_description = request.args.get("error_description") or ""

    if error:
        return jsonify({"error": error, "error_description": error_description}), 401

    try:
        payload= scalekit.authenticate_using_code(code)
        print("--------------------------------")
        print(f"payload: {payload}\n\n")

        scalekit_user = scalekit.get_user_info(payload["user"]["id"])
        print(f"scalekit_user: {scalekit_user}\n\n")

        user = UserCredentials(
            access_token=scalekit_user.get("access_token"),
            id_token=scalekit_user.get("id_token"),
            refresh_token=scalekit_user.get("refresh_token"),
            scalekit_user_id=scalekit_user.get("scalekit_user_id"),
        )

        print(f"user: {user}\n\n")

        return jsonify(user)

        # print(f"user: {user}\n\n")
        # current_user = user_service.upsert(user)
        # return jsonify(current_user)
    except Exception as err:
        print(f"Error exchanging code: {err}")
        return jsonify({"error": "Failed to authenticate user"}), 500


@app.route("/api/user/<int:id>")
def user(id: int):
    return jsonify(user_service.get(id))

if __name__ == "__main__":
    app.run(debug=True, port=3000)
