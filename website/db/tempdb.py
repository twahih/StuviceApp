import os 

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_login import UserMixin, current_user, login_user, logout_user, login_required, LoginManager
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from dotenv import load_dotenv

db = SQLAlchemy()

# Define models
class Completed_Service_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Service_Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Service_reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Service_requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class User_services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model

login_manager = LoginManager()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), primary_key=True)    
    __tablename__ = 'users'
    
    # ... user model fields here ...

    def verify_password(self, password):
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_user(email, password):
        """Create a new user."""
        user = Users(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        """Load a user given their ID."""
        return Users.query.get(int(user_id))

class Wall_Post_Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Wall_Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Wall_Post_Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model

from flask import current_app, g
import sqlite3


class Database:
    def __init__(self, dbname):
        self.dbname = dbname

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or [])
        return self.cursor

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def create_user(self, username, password):
        self.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.commit()

    def read_user(self, user_id=None, username=None):
        if user_id is not None:
            self.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        elif username is not None:
            self.execute("SELECT * FROM users WHERE username = ?", (username,))
        else:
            raise ValueError("Either user_id or username must be provided")

        return self.cursor.fetchone()

    def update_user(self, user_id, username=None, password=None):
        if username is not None:
            self.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
        if password is not None:
            self.execute("UPDATE users SET password = ? WHERE id = ?", (password, user_id))

        self.commit()

    def delete_user(self, user_id):
        self.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.commit()

    def create_post(self, title, content, author_id):
        self.execute("INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)", (title, content, author_id))
        self.commit()

    def read_post(self, post_id):
        self.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        return self.cursor.fetchone()

    def update_post(self, post_id, title=None, content=None):
        if title is not None:
            self.execute("UPDATE posts SET title = ? WHERE id = ?", (title, post_id))
        if content is not None:
            self.execute("UPDATE posts SET content = ? WHERE id = ?", (content, post_id))

        self.commit()

    def delete_post(self, post_id):
        self.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        self.commit()


class FlaskDatabase(Database):
    def __init__(self, dbname=None):
        self.dbname = dbname or current_app.config['DATABASE']

    @property
    def connection(self):
        if 'db' not in g:
            g.db = sqlite3.connect(self.dbname)
            g.db.row_factory = sqlite3.Row

        return g.db

    @property
    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def disconnect(self):
        if 'db' in g:
            g.db.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or [])
        return self.cursor

    def create_user(self, username, password):
        self.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.commit
