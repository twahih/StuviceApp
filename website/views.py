from flask import Blueprint, render_template,get_flashed_messages, request, redirect,flash, jsonify,url_for,session
from flask_login import login_required, current_user,login_user,logout_user
from .models import User,ServiceRequest,Friend
from sqlalchemy import or_


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('/index-register.html')

@views.route('/user/')
@login_required
def user(): 
    """This method is called after a user has been authenticated and it created a user json object and render the profile page"""
    if current_user:
        user = current_user.query.filter_by(user_id=current_user.user_id).first()
        if user:
            #session['user_id'] = User.user_id
            login_user(user, remember=True)
            user = current_user  # call create use method of User class to convert to json object
    
            return render_template('/newsfeed.html',user = current_user)
        else:
            return redirect(url_for('views.logout'))
    else:
        return render_template('index-register.html')

    

@views.route('/logout/')
#@login_required
def logout():
    logout_user()
    active_tab = 'login'
    return render_template('/index-register.html', active_tab = active_tab)

@views.route('/profile/Settings/')
@login_required
def settings():
    return render_template('/edit-profile-basic.html',user = current_user)

@views.route('/timeline')
@login_required
def timeline():
    return render_template('/BaseTimeline.html', user = current_user)



@views.route('/search_users', methods=['GET','POST'])
@login_required
def search_users():
    search = request.form.get('search')
    results = User.query.filter(or_(User.firstname.ilike(f'%{search}%'), User.email.ilike(f'%{search}%'))).all()
    users = [{'firstname': user.firstname,'lastname':user.lastname ,'email': user.email,'user_id':user.user_id} for user in results]
    return jsonify({'users': users})


@views.route('/public_profile/<int:user_id>')
def public_profile(user_id):
    user_profile = User.query.get_or_404(user_id)
    friend = Friend.query.filter_by(user_id=current_user.user_id, friend_id=user_id).first()

    if friend is None:
        friend = Friend.query.filter_by(user_id=user_id, friend_id=current_user.user_id).first()


    user_requests = ServiceRequest.query.filter_by(user_id=user_id).all()

    return render_template('/timeline-about.html', user=user_profile, friend=friend, user_requests=user_requests, service_id_to_request={r.service_id: r for r in user_requests})


@views.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    user_profile = User.query.filter_by(user_id=user_id).first()
    if not user_profile:
        flash('User not found', category='error')
        return redirect(url_for('views.timeline', user=current_user))
    if user_profile == current_user:
        return redirect(url_for('views.timeline', user=current_user))
    friend = Friend.query.filter_by(user_id=current_user.user_id, friend_id=user_id,status = 'accepted').first()
    if friend is None:
        friend = Friend.query.filter_by(user_id=user_id, friend_id=current_user.user_id,status = 'accepted').first()
    if friend:
        user_requests = ServiceRequest.query.filter_by(user_id=current_user.user_id).all()
        return render_template('/faq.html', user=user_profile, user_requests=user_requests, service_id_to_request={r.service_id: r for r in user_requests})
    else:
        user_requests = ServiceRequest.query.filter_by(user_id=current_user.user_id).all()
        return redirect(url_for('views.public_profile', user_id=user_profile.user_id))

