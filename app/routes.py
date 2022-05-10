from flask import render_template, url_for, flash, redirect, request
from . import app, db, bcrypt
from app.models import User, Pitch
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import Register, Login, PitchForm, CommentsForm
db.create_all()


def comments_cutter(string_comments):
    """Takes in a string cuts it and returns a list of comments
    """
    return string_comments.split(';')


@app.route('/')
def home():
    # All pitches here
    pitches = Pitch.query.all()

    # comments_list = comments_cutter(pitches.comments)
    return render_template('index.html', pitches=pitches)


@app.route('/comments/<id>',methods=['POST', 'GET'])
def comments(id):
    form = CommentsForm()
    pitch = Pitch.query.filter_by(id=id).first()
    form.content.data = "Your comment here"
    return render_template('comments.html', form=form , pitch=pitch)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account Has been Created! You are now able to login  in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/authentification/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.username.title()} !! ', 'success')
            # args is a dict
            # get returns none if the next key does not exist
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data,
                      content=form.content.data, user_id=current_user.id)
        db.session.add(pitch)
        db.session.commit()
        flash('Your pitch was successfully added')
        return redirect(url_for('home'))
    return render_template('create.html', form=form, title='New Pitch')


@app.route('/post/like/<int:pitchid>', methods=['GET'])
@login_required
def likes(pitchid):
    """
    Adds a like when click of a button

    Returns:
        _type_: _description_
    """

    pitch = Pitch.query.filter_by(id=pitchid).first()

    # update = pitch.likes + 1
    pitch.likes += 1
    pitch.dislikes -= 1
    db.session.commit()
    # return str(pitch.likes)
    return redirect(url_for('home'))


@app.route('/post/dislikes/<int:pitchid>', methods=['POST', 'GET'])
@login_required
def dislikes(pitchid):
    """
    Adds a dislikes when click of a button

    Returns:
        _type_: _description_
    """

    pitch = Pitch.query.filter_by(id=pitchid).first()

    pitch.dislikes += 1
    pitch.likes -= 1
    db.session.commit()
    return redirect(url_for('home'))
