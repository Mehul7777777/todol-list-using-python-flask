from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import Column, Integer, String
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# To create the database table
class Todo(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


db.create_all()


# now = datetime.now()
# current_date = now.strftime("%d/%m/%Y")


@app.route("/", methods=["POST", "GET"])
def start():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding a task'
    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)


@app.route("/remove/<int:id>")
def remove(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was an error while deleting that task'


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    task = Todo.query.get_or_404(id)
    remove(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return 'There was an error while updating that task'
    else:
        return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)