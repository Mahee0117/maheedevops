from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os


load_dotenv()

app = Flask(__name__)


# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")

print("MongoDB URI loaded:", mongo_uri is not None)

client = MongoClient(mongo_uri, tlsAllowInvalidCertificates=True)

db = client["student_database"]
collection = db["students"]


# Home page - show form
@app.route("/")
def home():
    return render_template("form.html")


# API route - read data from backend JSON file
@app.route("/api")
def api():

    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


# Form submission route
@app.route("/submit", methods=["POST"])
def submit():

    try:
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]

        student = {
            "name": name,
            "email": email,
            "department": department
        }

        collection.insert_one(student)

        return redirect(url_for("success"))

    except Exception as e:

        return render_template(
            "form.html",
            error=str(e),
            name=request.form.get("name", ""),
            email=request.form.get("email", ""),
            department=request.form.get("department", "")
        )


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)