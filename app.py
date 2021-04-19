from flask import Flask, render_template, redirect
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwekwqkJDHASIqwop'

def db_f():
    db.db_session.global_init("db/clever.db")
    db_sess = db.db_session.create_session()
    for user in db_sess.query(db.User).all():
        print(user)
    # db.main()

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/task')
def task():
    return render_template('task.html')

@app.route('/auth', methods=['GET', 'POST'])
def authPage():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('auth.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/panel/task/edit')
def edit_task():
    return render_template('taskedit.html')


if __name__ == "__main__":
    db_f()
    app.run(debug=True)
