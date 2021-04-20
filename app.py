from flask import Flask, render_template, redirect, request
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
import db
from data.users import User

db.db_session.global_init("db/clever.db")
db_sess = db.db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwekwqkJDHASIqwop'

def db_f():
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
        isteacher = request.form.get('isteacher')
        if isteacher:
            isteacher = 1
        else:
            isteacher = 0
        kwargs = {'name': form.firstname.data, 'surname': form.lastname.data, 'email': form.email.data, 'password': form.password.data, 'status': isteacher}
        user = db.add_user(db_sess=db_sess, **kwargs)
        # if form.password.data != form.passwordRepeat.data:
        #     print(form.data)
        #     return render_template('register.html', form=form, message='Пароли не совпадают!')
        return redirect('/auth')
    return render_template('register.html', form=form)


@app.route('/panel/task/edit')
def edit_task():
    return render_template('taskedit.html')


if __name__ == "__main__":
    db_f()
    app.run(debug=True)
