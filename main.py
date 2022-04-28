from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'youdidnthearitfrommebut'
db = SQLAlchemy(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])

    submit = SubmitField("Submit")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=True, nullable=False)
    is_complete = db.Column(db.Boolean, default=False, nullable=False)


db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    tasks = db.session.query(Task).all()
    form = TaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_task = Task(
                task=form.task.data
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('index.html', form=form, tasks=tasks)


@app.route("/delete/<int:task_id>", methods=["POST", "GET"])
def delete_task(task_id):
    post_to_delete = Task.query.get(task_id)
    print(post_to_delete.is_complete)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/complete/<int:task_id>", methods=["POST", "GET"])
def complete_task(task_id):
    completed_task = Task.query.get(task_id)
    completed_task.is_complete = True
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
