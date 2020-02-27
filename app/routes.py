from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.forms import LoginForm, ProjectForm
from app.models import User, Project
import os
from datetime import datetime
from PIL import Image


def save_picture(form_picture):
    """ Save (resized) image to the filesystem with a unique (random) name. """
    # Create a random file name.
    # random_string = uuid4().hex
    # _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = 'img/' + form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/', picture_filename)

    # Save image to filesystem.
    img = Image.open(form_picture)
    img.save(picture_path)

    # Return filename so we can save it to the database.
    return picture_filename


def save_update_project(form, project_id=None):
    """ Save or update a project. """
    if project_id is None:
        project = Project()
    else:
        project = Project.query.get(project_id)

    project.title = form.title.data.title()
    project.description = form.description.data
    if form.thumbnail.data is not None:
        picture_file = save_picture(form.thumbnail.data)
        project.thumbnail = picture_file
    project.hide = form.hide.data
    project.order_number = form.order_number.data
    project.overlay_title = form.overlay_title.data.upper()
    project.overlay_text = form.overlay_text.data.upper()
    project.link = form.link.data
    project.updated_at = datetime.now()

    return project


@login_manager.user_loader
def load_user(user_id):
    """ Because Flask-Login knows nothing about databases, it needs the application's help in loading a user.
    For that reason, the extension expects that the application will configure a user loader function,
     that can be called to load a user given the ID. """
    return User.query.get(int(user_id))


@app.route("/")
def index():
    projects = Project.query.order_by(Project.order_number).all()
    return render_template("index.html", projects=projects)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # For GET requests, show the login form.
    # For POST requests, check if user may login.
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password!", "danger")
                return redirect(url_for('login'))
            else:
                login_user(user)
                flash("Login successful.", "success")
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form=form)


@app.route("/dashboard")
@app.route("/dashboard/")
@login_required
def dashboard():
    return render_template("dashboard/dashboard_home.html")


@app.route("/dashboard/projects", methods=['GET'])
@app.route("/dashboard/projects/", methods=['GET'])
@login_required
def dashboard_projects_index():
    projects = Project.query.order_by(Project.order_number).all()
    return render_template("dashboard/projects.html", projects=projects)


@app.route("/dashboard/projects/create", methods=['GET'])
@login_required
def dashboard_projects_create():
    return render_template("dashboard/projects_create.html", form=ProjectForm())


@app.route("/dashboard/projects/store", methods=['POST'])
@login_required
def dashboard_projects_store():
    form = ProjectForm()
    if form.validate_on_submit():
        project = save_update_project(form)
        db.session.add(project)
        db.session.commit()
        flash(f"Added a new project.", "success")
        return redirect('/dashboard/projects')
    else:
        return render_template("dashboard/projects.html")


@app.route("/dashboard/projects/<project_id>/edit", methods=['GET'])
@login_required
def dashboard_projects_edit(project_id):
    project = Project.query.get(project_id)
    if project is None:
        return "Resource not found!", 404  # todo render a 404.html
    else:
        form = ProjectForm()
        form.title.data = project.title
        form.description.data = project.description
        form.thumbnail.data = project.thumbnail
        form.hide.data = project.hide
        form.order_number.data = project.order_number
        form.link.data = project.link
        form.overlay_title.data = project.overlay_title
        form.overlay_text.data = project.overlay_text

        return render_template("dashboard/projects_edit.html", form=form, project_id=project.id)


@app.route("/dashboard/projects/<project_id>", methods=['POST', 'PUT'])
@login_required
def dashboard_projects_update(project_id):
    form = ProjectForm()
    if form.validate_on_submit():
        project = save_update_project(form, project_id=project_id)
        db.session.commit()
        flash(f'Updated project "{project.title}".', "success")
        return redirect('/dashboard/projects')
    else:
        return render_template(f"dashboard/projects/{project_id}/edit.html")


@app.route("/dashboard/projects/<project_id>/delete", methods=['POST', 'DELETE'])
@login_required
def dashboard_projects_delete(project_id):
    project = Project.query.filter_by(id=project_id).first()
    title = project.title
    db.session.delete(project)
    db.session.commit()
    flash(f'Deleted project "{title}".', "success")
    return redirect('/dashboard/projects')


@app.route("/dashboard/projects/order", methods=['POST'])
@login_required
def projects_order():
    """ Save projects order send by an ajax request. """

    ordered_project_ids = request.json['ordered_project_ids']

    for i, project_id in enumerate(ordered_project_ids):
        project = Project.query.get(project_id)
        project.order_number = i

    db.session.commit()

    return "Updated projects order."


@app.route("/dashboard/subscriptions")
@login_required
def dashboard_subscriptions():
    return render_template("dashboard/subscriptions.html")


@app.route("/dashboard/notify")
@login_required
def dashboard_notify():
    return render_template("dashboard/notify.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
