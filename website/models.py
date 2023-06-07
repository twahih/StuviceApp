import os

from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import  fields
from flask_marshmallow import Marshmallow
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv('config.env')

db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url.format(
    username="root",
    password="Twahih199400.",
    host="localhost",
    port="3306",
    database="stuvicedb"
))


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    phone = db.Column(db.String(15))
    about_me = db.Column(db.String(255))
    sex = db.Column(db.String(10))
    school = db.Column(db.String(128))
    date_of_birth = db.Column(db.DateTime)
    status = db.Column(db.Boolean, default= 'active')
    posts = db.relationship('WallPost', back_populates='user', lazy=True)
    services = db.relationship('UserServices', back_populates='user',lazy = True)
    service_requests = db.relationship('ServiceRequest', back_populates='user',lazy = True)
    #services = db.relationship('Service', secondary='user_services' , back_populates='users')
    #messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='users')

    @staticmethod
    def connect_to_db(db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        return Session()

    @staticmethod
    def create_db_user(user_data):
        session = db.session()
        result = session.execute(text('CALL create_user(:firstname, :lastname, :email, :password, :phone, :sex, :school, :date_of_birth)'), user_data)
        session.commit()
        return result

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.user_id)

    @staticmethod
    def get_by_id(user_id):
        session = db.session()
        result = session.execute('CALL get_user_by_id(:user_id)', {'user_id': user_id})
        return result.fetchone()
    @staticmethod
    def get_id_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user.user_id if user else None
    
    def friend_status(self, other_user):
        friend = Friend.query.filter(
            ((Friend.user_id == self.user_id) & (Friend.friend_id == other_user.user_id)) |
            ((Friend.user_id == other_user.user_id) & (Friend.friend_id == self.user_id))
        ).order_by(Friend.created_at.desc()).first()
        
        if friend is None:
            return None
        
        return friend.status
    
    def unread_notification_count(self):
        return Notification.query.filter_by(recipient=self, is_read=False).count()
    def all_notifications(self):
        return Notification.query.filter_by(recipient=self).order_by(Notification.is_read.asc(), Notification.created_at.desc()).all()

    def update(self,user_data):
        update_query = text("CALL update_user(:user_id,:firstname, :lastname, :email,:phone, :school, :sex, :date_of_birth,:about_me)")
        session = db.session()
        resutls = session.execute(update_query, user_data)
        session.commit()
        return resutls

    def delete(self):
        session = db.session()
        session.execute('CALL delete_user(:user_id)', {'user_id': self.id})
        session.commit()

    def add_post(self, post):
        session = db.session()
        session.execute('CALL add_post_to_user(:user_id, :post_id)', {'user_id': self.id, 'post_id': post.id})
        session.commit()

    def remove_post(self, post):
        session = db.session()
        session.execute('CALL remove_post_from_user(:user_id, :post_id)', {'user_id': self.id, 'post_id': post.id})
        session.commit()

    def add_service(self, service_data):
        add_query = text("CALL add_service_to_user(:user_id, :category_name_in, :service_name,:price ,:description)")
        session = db.session()
        results = session.execute(add_query, service_data)
        session.commit()
        return results

    def remove_service(self, service):
        session = db.session()
        session.execute('CALL remove_service_from_user(:user_id, :service_id)', {'user_id': self.id, 'service_id': service.id})
        session.commit()
    def send_message(self, receiver, content):
        session = db.session()
        session.execute('CALL send_message(:sender_id, :receiver_id, :content)', {'sender_id': self.id, 'receiver_id': receiver.id, 'content': content})
        session.commit()

    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(user_id):
        session = db.session()
        result = session.execute(text('CALL get_user_by_id(:user_id)'), {'user_id': user_id})
        session.commit()
        user_data = result.fetchone()
        if user_data:
            user = User(user_id=user_data.user_id, firstname=user_data.firstname,lastname=user_data.lastname, email=user_data.email, phone=user_data.phone, sex=user_data.sex, school=user_data.school, date_of_birth=user_data.date_of_birth, status=user_data.status)
            return user
        else:
            return None


# Define models
class CompletedServiceRequest(db.Model):
    __tablename__ = 'completed_service_requests' 
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class Friend(db.Model):
    __tablename__ = 'friends' 
    user_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('pending', 'accepted', 'declined'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Add relevant columns for this model
    
class Message(db.Model):
    __tablename__ = 'messages' 
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model

class ServiceCategory(db.Model):
    __tablename__ = 'service_categories' 
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(128), nullable=False)
    services = db.relationship('UserServices', backref='category_services')

class UserServices(db.Model):
    __tablename__ = 'user_services' 
    service_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.category_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    service_name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    averagerate = db.Column(db.Float, nullable=False)
    user = db.relationship('User', back_populates='services')
    category = db.relationship('ServiceCategory', foreign_keys=[category_id], backref='category_services')
    service_requests = db.relationship('ServiceRequest', back_populates='user_service', lazy=True)



    def update_service(self,service_data):
        update_query = text("CALL update_service(:service_id,:category_name_in, :service_name,:price,:description)")
        session = db.session()
        results = session.execute(update_query, service_data)
        session.commit()
        return results
    

    
    
class ServiceReview(db.Model):
    __tablename__ = 'service_reviews'   
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    request_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('user_services.service_id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    to_date = db.Column(db.DateTime, nullable=False)
    from_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'in_progress', 'declined', 'complete'), primary_key= True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', back_populates='service_requests')
    
    user_service = db.relationship('UserServices', back_populates='service_requests')

    def submit_request(self,service_request_data):
        add_request_sql = text("""
        CALL add_service_request(:service_id, :message, :to_date, :from_date, :user_id, :service_name,:price);
        """)
        session = db.session()
        results = session.execute(add_request_sql, service_request_data)
        session.commit()
        return results
    def update_request(self, service_request_data):
        update_request_sql = text("""
        CALL update_service_request(:request_id, :service_id, :message, :to_date, :from_date, :user_id);
        """)
        session = db.session()
        results = session.execute(update_request_sql, service_request_data)
        session.commit()
        return results

    def cancel_request(self, request_id):
        cancel_request_sql = text("""
        CALL cancel_service_request(:request_id);
        """)
        session = db.session()
        results = session.execute(cancel_request_sql, {'request_id': request_id})
        session.commit()
        return results

    def start_request(self, request_id):
        start_request_sql = text("""
        CALL start_service_request(:request_id);
        """)
        session = db.session()
        results = session.execute(start_request_sql, {'request_id': request_id})
        session.commit()
        return results

    def end_request(self, request_id):
        end_request_sql = text("""
        CALL end_service_request(:request_id);
        """)
        session = db.session()
        results = session.execute(end_request_sql, {'request_id': request_id})
        session.commit()
        return results
    
    def get_service_requests_by_user_id(self, user_id):
        return self.query.filter_by(user_id=user_id).all()



    

login_manager = LoginManager()


class WallPostLike(db.Model):
    __tablename__ = 'wall_posts_' 
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model
    
class WallPost(db.Model):
    __tablename__ = 'wall_posts_likes' 
    wall_post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User',back_populates='posts')
    # Add relevant columns for this model
    
class WallPostComment(db.Model):
    __tablename__ = 'wall_posts_comments' 
    id = db.Column(db.Integer, primary_key=True)
    # Add relevant columns for this model


class Notification(db.Model):
    __tablename__ = 'user_notifications'
    id = db.Column(db.Integer, db.ForeignKey('user_services.service_id'),nullable=True)  
    notification_id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    notification_type = db.Column(db.Enum('friends', 'service', 'group'), nullable=False)

    recipient = db.relationship('User', foreign_keys=[recipient_id])
    sender = db.relationship('User', foreign_keys=[sender_id])
    service = db.relationship('UserServices', foreign_keys=[id])



class UserCreationError(Exception):
    pass



