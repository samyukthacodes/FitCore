import pymongo
from pymongo.errors import ConnectionFailure
import bcrypt
import streamlit as st
import os
from dotenv import load_dotenv


def get_mongo_client():
    load_dotenv()
    try:
        connection_string = st.secrets["CONNECTION_STRING"]
        # Replace with your MongoDB Atlas connection string
        client = pymongo.MongoClient(connection_string)
        client.server_info()  # To check if the connection is successful
        return client
    except ConnectionFailure as e:
        print("Could not connect to MongoDB:", e)
        return None

def authenticate_user(username, password):
    """Authenticate a user with the provided username and password."""
    client = get_mongo_client()
    if client:
        db = client['fitCore_user_data']  # Database name
        users_collection = db['users']  # Collection name

        # Find user by username
        user = users_collection.find_one({"username": username})
        stored_hashed_password = user['password']
        # Check if user exists and password matches
        if user and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            st.session_state["username"] = username
            st.session_state["db"]  = db
            return True
    return False



def add_user(username, password):
    client = get_mongo_client()
    if client:
        db = client['fitCore_user_data']  # Database name
        users_collection = db['users']  # Collection name

        # Check if username already exists
        if users_collection.find_one({"username": username}):
            return False
        else:
            # Insert new user
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            users_collection.insert_one({"username": username, "password": hashed_password})
            return True
        
def get_user_workouts(username):
    """Retrieve user workouts from the database."""
    client = get_mongo_client()
    if client:
        db = client['fitCore_user_data']  # Database name
        users_collection = db['users']  # Collection name
        user = users_collection.find_one({"username": username})
        return user.get("workouts", [])

def add_workout_to_user(username, workout):
    """Add a new workout routine for the user."""
    client = get_mongo_client()
    if client:
        db = client['fitCore_user_data']  # Database name
        users_collection = db['users']  # Collection name


        users_collection.update_one(
            {"username": username},
            {"$push": {"workouts": workout}}
        )
