import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from db import models

load_dotenv('config.env')  # Load environment variables from config.env file 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


# Define routes and views
@app.route('/completed-service-requests')
def list_completed_service_requests():
    requests = models.CompletedServiceRequest.query.all()
    return jsonify([request.serialize() for request in requests])

@app.route('/friends', methods=['POST'])
def add_friend():
    # Parse request data and create new Friend object
    friend = models.Friend(...)
    db.session.add(friend)
    db.session.commit()
    return jsonify(friend.serialize())

@app.route('/messages', methods=['POST'])
def send_message():
    # Parse request data and create new Message object
    message = models.Message(...)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.serialize())

@app.route('/service-categories')
def list_service_categories():
    categories = models.ServiceCategory.query.all()
    return jsonify([category.serialize() for category in categories])

@app.route('/service-reviews', methods=['POST'])
def leave_service_review():
    # Parse request data and create new ServiceReview object
    review = models.ServiceReview(...)
    db.session.add(review)
    db.session.commit()
    return jsonify(review.serialize())

@app.route('/service-requests', methods=['POST'])
def create_service_request():
    # Parse request data and create new ServiceRequest object
    request = models.ServiceRequest(...)
    db.session.add(request)
    db.session.commit()
    return jsonify(request.serialize())

@app.route('/user-services')
def list_user_services():
    services = models.UserServices.query.all()
    return jsonify([service.serialize() for service in services])

@app.route('/users', methods=['POST'])
def create_user():
    # Parse request data and create new User object
    user = models.User(...)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route('/wall-post-likes', methods=['POST'])
def like_wall_post():
    # Parse request data and create new WallPostLike object
    like = models.WallPostLike(...)
    db.session.add(like)
    db.session.commit()
    return jsonify(like.serialize())
