from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from .models import User,UserCreationError,UserServices,ServiceRequest,Friend,Notification
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from flask_wtf.csrf import generate_csrf




auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """This method recieve a login form and and check if the user exists and redirect the user to views with the user ID"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            # verify password if the email is correct
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
   
                return redirect(url_for('views.user'))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('views.logout'))
            
    flash('Incorrect email or password','danger')
    return redirect(url_for('views.logout'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """This method receive a posted form for signum, validate it and add a new user to the database else redirect to registeration form"""

    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        phone = request.form.get('phone')
        sex = '1' if request.form.get('gender') =='male' else '0'
        school = request.form.get('school')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        from datetime import datetime
        try: 
            date_of_birth = datetime.strptime(f"{year}-{month}-{day}", "%Y-%b-%d")
        except ValueError as e:
            flash('Invalid date format.' + day + month + year, category='error')
            raise e

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != password:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user_data = {
                        'firstname': firstname,
                        'lastname': lastname,
                        'email': email,
                        'password': generate_password_hash(password, method='sha256'),
                        'phone': phone,  # in the future use hashing instead
                        'sex': sex,
                        'school': school,
                        'date_of_birth': date_of_birth
                        }
            # create a user sql object 
            new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password, method='sha256'), phone=phone, sex=sex, school=school,date_of_birth = date_of_birth)
            try:
                # add the new user to the database
                result = new_user.create_db_user(user_data)
                if result.rowcount == 1:
                    new_user_id = User.get_id_by_email(email)
                    user = User.load_user(new_user_id)
                    login_user(user, remember=True)
                    flash('Account created!', category='success')
                    return redirect(url_for('views.user',user = current_user))
            except Exception as e:
                db.session.rollback()
                flash('Error creating account.', category='error')
                raise UnboundLocalError(str(e))

    return render_template("index-register.html", user=current_user)

@auth.route('/update_basic_info/', methods=['GET', 'POST'])
@login_required
@login_required
def update_basic_info():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        about_me = request.form.get('aboutme')
        phone = request.form.get('phone')
        sex = '1' if request.form.get('gender') =='male' else '0'
        school = request.form.get('school')
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
        from datetime import datetime
        try: 
            date_of_birth = datetime.strptime(f"{year}-{month}-{day}", "%Y-%b-%d")
        except ValueError as e:
            flash('Invalid date format.' + day + month + year, category='error')
            raise e

        email_exists = User.query.filter_by(email=email).first()
        if email_exists and email_exists.user_id != current_user.user_id:
            flash('The email address is already in use.', category='error')
            return redirect(url_for('views.user', user=current_user))

        user_data = {
                        'user_id': current_user.user_id,
                        'firstname': firstname,
                        'lastname': lastname,
                        'email': email,
                        'phone': phone,
                        'school': school,
                        'sex': sex,
                        'date_of_birth': date_of_birth,
                        'about_me': about_me,                         
                        }

        if current_user:
            try:
                result = current_user.update(user_data)
                if result.rowcount == 1:
                    user = User.load_user(current_user.user_id)
                    login_user(user, remember=True)
                    flash('Basic info updated!', category='success')
                    return redirect(url_for('views.timeline',user = current_user))
            except IntegrityError as e:
                db.session.rollback()
                if "Duplicate entry" in str(e) and "for key 'users.email'" in str(e):
                    flash('The email address is already in use.', category='error')
                else:
                    flash('Error updating account.', category='error')
            except Exception as e:
                db.session.rollback()
                flash('Error updating account.', category='error')
            return redirect(url_for('views.user',user = current_user))

        
@auth.route('/add_service', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        service_name = request.form.get('service_name')
        description = request.form.get('service_description')
        price = request.form.get('service_price')
        category_name = request.form.get('service_category')
        user_id = current_user.user_id
        service_data = {
                        'user_id': user_id,
                      'service_name': service_name,
                      'price': price,
                      'description': description,
                      'category_name_in': category_name,
                        }
        if current_user:
            try:
                result = current_user.add_service(service_data)
                if result.rowcount == 1:
                    user = User.load_user(current_user.user_id)
                    login_user(user, remember=True)
                    flash('Service added!', category='success')
                    return redirect(url_for('views.timeline',user = current_user))
            except Exception as e:
                db.session.rollback()
                flash('Error adding service.', category='error')
                raise UnboundLocalError(str(e))
            return redirect(url_for('views.user',user = current_user))

@auth.route('/delete_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def delete_service(service_id):
    # Retrieve the service using the service_id
    service = UserServices.query.get_or_404(service_id)

    # Delete the service from the database
    db.session.delete(service)
    db.session.commit()

    # Redirect to a success page or the page displaying services
    return redirect(url_for('views.timeline',user = current_user))

@auth.route('/update_service', methods=['GET', 'POST'])
@login_required
def update_service():
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        service_name = request.form.get('service_name')
        price = request.form.get('service_price')
        description = request.form.get('service_description')
        category_name = request.form.get('service_category')
        user_id = current_user.user_id
        service_data = {
                        'user_id': user_id,
                     'service_id': service_id,
                     'service_name': service_name,
                      'price': price,
                      'description': description,
                      'category_name_in': category_name,
                        }
        service = UserServices.query.get_or_404(service_id)
        if service:
            try:
                result = service.update_service(service_data)
                if result.rowcount == 1:
                    flash('Service updated!', category='success')
                    return redirect(url_for('views.timeline',user = current_user))
            except Exception as e:
                db.session.rollback()
                flash('Error updating service.', category='error')
                raise UnboundLocalError(str(e))
            return redirect(url_for('views.timeline',user = current_user))

@auth.route('/submit_request', methods=['GET', 'POST'])
@login_required
def submit_request():
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        message = request.form.get('message')
        to_date = request.form.get('to_date')
        from_date = request.form.get('from_date')
        service_name = request.form.get('service_name')
        price = request.form.get('service_price')
        user_id = current_user.user_id
        service = UserServices.query.get_or_404(service_id)
        user = User.query.get_or_404(user_id)
        service_request_data = {'service_id': service_id, 'message': message, 'to_date': to_date, 'from_date': from_date,'user_id': user_id, 'service_name': service_name,'price': price}

        if service:
            try:
                result = ServiceRequest().submit_request(service_request_data)
                user_profile_id = service.user.user_id
                if result.rowcount == 1:
                    flash('Request submitted!', category='success')
                    return redirect(url_for('views.user_profile',user_id = user_profile_id))
            except Exception as e:
                db.session.rollback()
                flash('Error submitting request.', category='error')
                raise UnboundLocalError(str(e))
            return redirect(url_for('views.timeline',user = current_user))
        
@auth.route('/update_request', methods=['GET', 'POST'])
@login_required
def update_request():
    if request.method == 'POST':
        print('Updating request')
        submit_type = request.form.get('submit_type')
        request_id = request.form.get('request_id')
        service_id = request.form.get('service_id')
        message = request.form.get('message')
        to_date = request.form.get('to_date')
        from_date = request.form.get('from_date')
        service_name = request.form.get('service_name')
        user_id = current_user.user_id
        service = UserServices.query.get_or_404(service_id)
        user = User.query.get_or_404(user_id)
        service_request_data = {'request_id': request_id, 'service_id': service_id, 'message': message, 'to_date': to_date, 'from_date': from_date, 'user_id': user_id}
        action = 'unknown'
        if service:
            try:
                if submit_type == 'update':
                    result = ServiceRequest().update_request(service_request_data)
                    action = 'updated'
                elif submit_type == 'cancel':
                    result = ServiceRequest().cancel_request(request_id)
                    action = 'canceled'
                
                user_profile_id = service.user.user_id
                if result.rowcount == 1:
                    flash(f'Request {action}!', category='success')
                    return redirect(url_for('views.user_profile', user_id=user_profile_id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error {action} request.', category='error')
                raise UnboundLocalError(str(e))
            return redirect(url_for('views.timeline', user=current_user))
        
    else:
        return redirect(url_for('views.timeline', user=current_user))
    # Add logic for handling GET requests or other methods if needed.

@auth.route('/friend_request', methods=['POST'])
@login_required
def friend_request():
    user_id = request.form.get('user_id')
    user_profile = User.query.get_or_404(user_id)
    friend = Friend.query.filter_by(user_id=current_user.user_id, friend_id=user_profile.user_id).first()
    if not friend:
        friend = Friend(user_id=current_user.user_id, friend_id=user_profile.user_id)
        db.session.add(friend)
        db.session.commit()
        flash('Friend request sent to {}.'.format(user_profile.firstname), 'success')
    return redirect(url_for('views.user_profile', user_id=user_id))

@auth.route('/cancel_friend_request', methods=['POST'])
@login_required
def cancel_friend_request():
    user_id = request.form.get('user_id')
    friend = Friend.query.filter_by(user_id=current_user.user_id, friend_id=user_id).first()
    if friend:
        db.session.delete(friend)
        db.session.commit()
        flash('Friend request cancelled', category='success')
        redirect(url_for('views.user_profile', user_id=user_id))
    else:
        flash('Friend request not found', category='error')
    return redirect(url_for('views.user_profile', user_id=user_id))

@auth.route('/respond_friend_request', methods=['POST'])
@login_required
def respond_friend_request():
    user_id = request.form.get('user_id')
    friend = Friend.query.filter_by(user_id=user_id, friend_id=current_user.user_id).first()
    if friend is None:
        friend= Friend.query.filter_by(user_id=current_user.user_id, friend_id=user_id).first()
    status = request.form.get('status')
    if status == 'accepted':
        friend.status = 'accepted'
    elif status == 'declined':
        friend.status = 'declined'
    else:
        flash('Invalid status', category='error')
    db.session.add(friend)
    db.session.commit()
    flash('Your response to the friend request has been saved.')
    return redirect(url_for('views.user_profile', user_id=user_id))



@auth.route('/unfriend/<int:user_id>', methods=['POST'])
def unfriend_user(user_id):
    # Delete the friend relationship from the database
    friend = Friend.query.filter_by(user_id=current_user.user_id, friend_id=user_id).first()
    if friend is None:
        friend = Friend.query.filter_by(user_id=user_id, friend_id = current_user.user_id).first()
    if friend:
        db.session.delete(friend)
        db.session.commit()
    
    # Redirect back to the user's profile page
    return redirect(url_for('views.public_profile', user_id=user_id))

@auth.route('/respond_to_friend_request_notification', methods=['POST'])
def respond_to_friend_request_notification():
    if request.method == 'POST':
        # Retrieve data from the request
        notification_id = request.form.get('notification_id')
        notification = Notification.query.get(notification_id)
        user_id = notification.sender.user_id

        friend = Friend.query.filter_by(user_id=user_id, friend_id=current_user.user_id).first()

        if friend is None:
            friend= Friend.query.filter_by(user_id=current_user.user_id, friend_id=user_id).first()
        
    status = request.form.get('action')
    if status == 'accepted':
        friend.status = 'accepted'
    elif status == 'declined':
        friend.status = 'declined'
    else:
        flash('Invalid ' + status, category='error')
    db.session.add(friend)
    db.session.commit()
    flash('Your response to the friend request has been saved.')
    return redirect(url_for('views.user_profile', user_id=user_id))

@auth.route('/update_notification_status', methods=['POST'])
@login_required
def update_notification_status():
    notification_id = request.form['notification_id']
    is_read = request.form['is_read']
    is_read = True if is_read == 'true' else False

    notification = Notification.query.get(notification_id)

    if notification:
        notification.is_read = is_read
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid notification or unauthorized'})

@auth.route('/respond_to_service_request_notification', methods=['POST'])
@login_required
def respond_to_service_request_notification():
    sender_id = request.form.get('sender_id')
    action = request.form.get('action')
    service_id = request.form.get('service_id')

    # Retrieve the notification and service objects from the database using the notification_id
    service_request = ServiceRequest.query.filter_by(user_id=sender_id,service_id=service_id ,status='pending').first()

    # Update the service request status based on the action
    if action == 'accepted':
        new_service_request = ServiceRequest(
        request_id = service_request.request_id,
        service_id=service_id,
        user_id = current_user.user_id,
        price = request.form.get('service_price'),
        message=request.form.get('message'),
        to_date=request.form.get('to_date'),
        from_date=request.form.get('from_date'),
        status='accepted'
        )
        # Set the service request as accepted
            # Save the changes to the database
        db.session.add(new_service_request)
        db.session.commit()

    elif action == 'declined':
        new_service_request = ServiceRequest(
        request_id = service_request.request_id,
        service_id=service_request.service_id,
        user_id = current_user.user_id,
        message=request.form.get('message'),
        to_date=request.form.get('to_date'),
        from_date=request.form.get('from_date'),
        status='declined'
        )
        db.session.add(new_service_request)
        db.session.commit()
    else:
        # Handle any other action or invalid input
        flash("Invalid action.", "danger")
        return jsonify({'success': False, 'error': 'Invalid action or unauthorized'})

    flash(f"Service request has been {action}.", "success")
    return jsonify({'success': True})