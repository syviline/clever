from flask import Flask, render_template, redirect, request
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.classcreate import ClassCreate
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import db
import uuid
import json
from data.users import User
from data.tests import Test
from data.userAnswers import UserAnswer
from data.classes import Class, class_to_test

db.db_session.global_init("db/clever.db")

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'qwekwqkJDHASIqwop'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db.db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:  # если пользователь авторизован
        if current_user.status == 1:  # если пользователь является учителем, то отправляем в панель управления классами и тестами
            return redirect('/panel')
        return redirect('/schoolar')  # в ином случае в панель ученика
    return render_template('landing.html')


# @app.route('/task')
# @login_required
# def task():
#     return render_template('task.html')


@app.route('/auth', methods=['GET', 'POST'])
def authPage():
    form = LoginForm()
    if form.validate_on_submit():  # авторизация
        db_sess = db.db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):  # если совпали логин и пароль
            login_user(user, remember=True)
            return redirect('/')
        return render_template('auth.html', form=form, message="Неправильный логин или пароль")
    return render_template('auth.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    form = RegisterForm()
    if form.validate_on_submit():
        isteacher = request.form.get('isteacher')  # проверяем галочку на поле "Зарегистрироваться как учитель"
        if isteacher:
            isteacher = 1
        else:
            isteacher = 0
        kwargs = {'name': form.firstname.data, 'surname': form.lastname.data, 'email': form.email.data,
                  'password': form.password.data, 'status': isteacher}
        db_sess = db.db_session.create_session()
        user = db.add_user(db_sess=db_sess, **kwargs)
        if user == -10:
            return render_template('register.html', form=form, message='Почта неправильная либо уже существует.')
        # if form.password.data != form.passwordRepeat.data:
        #     print(form.data)
        #     return render_template('register.html', form=form, message='Пароли не совпадают!')
        return redirect('/auth')
    return render_template('register.html', form=form)


@app.route('/panel')
@login_required
def panel():
    if current_user.status == 1:
        return redirect(
            "/panel/classes")  # у нас нет просто /panel, есть только /panel/classes и /panel/tests, по этому редиктерим юзера на /panel/classes если он зайдет на /panel
    return redirect("/schoolar")


@app.route('/panel/classes')
@login_required
def panel_classes():
    error = request.args.get('error')
    if current_user.status != 1:  # этот код сейчас будет везде, отправляет ученика, который забрел не туда, на страницу ученика.
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    classes = db_sess.query(Class).filter(Class.user_id == current_user.id)  # список классов учителя
    return render_template('panelclasses.html', title='Классы', classes=classes, error=error)


@app.route('/panel/classes/new', methods=['GET', 'POST'])
@login_required
def new_class():
    if current_user.status != 1:
        return redirect("/schoolar")
    form = ClassCreate()
    if request.method == 'POST':  # создание нового класса
        title = form.name.data
        class_ = Class()
        class_.title = title
        class_.user_id = current_user.id
        class_.invitation_link = uuid.uuid4().hex
        db_sess = db.db_session.create_session()
        db_sess.add(class_)
        db_sess.commit()
        return redirect('/panel/classes')
    return render_template('newclass.html', title='Новый класс', form=form)


@app.route('/panel/tests')
@login_required
def panel_tests():
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    tests = db_sess.query(Test).filter(Test.user_id == current_user.id).all()  # возвращает уже созданные учителем тесты
    print(tests)
    return render_template('paneltests.html', tests=tests)


@app.route('/panel/tests/new', methods=['GET', 'POST'])
@login_required
def new_test():
    if current_user.status != 1:
        return redirect("/schoolar")
    form = ClassCreate()  # использую форму для создания класса, зачем создавать новую форму если они будут одинаковые
    if request.method == 'POST':
        title = form.name.data
        test = Test()
        test.title = title
        test.task = '[{}]'
        test.user_id = current_user.id
        test.answers = '{}'
        test.scores = '{}'
        db_sess = db.db_session.create_session()
        db_sess.add(test)
        db_sess.commit()
        return redirect('/panel/tests')
    return render_template('newtest.html', form=form)


@app.route('/panel/class/<int:id>')
@login_required
def class_panel(id):  # информация о классе(ученики, тесты)
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    class_info = db_sess.query(Class).filter(Class.id == id).first()
    if class_info.user_id != current_user.id:
        return redirect('/panel/classes')
    schoolars = class_info.users
    restests = []  # создаю этот массив, чтобы разделить открытые тесты, и неоткрытые тесты по двум вкладкам
    tests = db_sess.query(Test).filter(Test.user_id == current_user.id).filter(Test.is_completable)
    opentests = class_info.tests
    for i in tests:
        if i not in opentests:  # те тесты которые открыты, будут в другой вкладке
            restests.append(i)
    print(opentests)
    return render_template('class.html', title=class_info.title, schoolars=schoolars, classid=id,
                           invitation_link=class_info.invitation_link, tests=restests, opentests=opentests)


@app.route('/opentest/<int:testid>/<int:classid>')
@login_required
def opentest(testid, classid):  # открывает тест для класса
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == testid).first()
    class_ = db_sess.query(Class).filter(Class.id == classid).first()
    if class_.user_id == current_user.id:  # проверяем чтобы и класс и тест принадлежали этому учителю
        if test.user_id == current_user.id:
            class_.tests.append(test)
    db_sess.commit()
    return redirect('/panel/class/' + str(classid))


@app.route('/closetest/<int:testid>/<int:classid>')
def closetest(testid, classid):
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == testid).first()
    class_ = db_sess.query(Class).filter(Class.id == classid).first()
    if class_.user_id == current_user.id:  # проверяем чтобы и класс и тест принадлежали этому учителю
        if test.user_id == current_user.id:
            class_.tests.remove(test)
            db_sess.commit()
    return redirect('/panel/class/' + str(classid))


@app.route('/logout')
@login_required
def logout():  # выход из аккаунта
    logout_user()
    return redirect('/')


@app.route('/panel/test/<int:id>')
@login_required
def edit_task(id):
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == id).first()  # изменение теста
    if test.user_id != current_user.id:  # проверяет чтобы тест принадлежал учителю
        return redirect('/panel/tests')
    print(test.task)
    # без json.loads, jinja2 заменяет все кавычки на &#(что-то там)
    return render_template('taskedit.html', task=json.loads(test.task), scores=json.loads(test.scores),
                           correctAnswersIds=json.loads(test.answers), testid=test.id)


@app.route('/taskedit/save', methods=['POST'])
@login_required
def save_task():  # сохранение теста(также происхожит каждые 5 секунд)
    testjson = request.json
    db_sess = db.db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == testjson['testid']).first()
    if test.user_id != current_user.id:
        return 'unauthorized'
    # анализируем task, если есть пустые задания или пустые ответы то задание нельзя будет отдать ученику
    is_completable = True  # можно ли отдавать задание ученику
    for index, row in enumerate(testjson['task']):
        if not row:
            is_completable = False
            continue
        if row['taskType'] == 'oneAnswer' or row['taskType'] == 'multipleAnswer':
            if not row['content']['answers']:
                is_completable = False
                continue
            if len(row['content']['answers']) == 0 or len(
                    row['content']['answers']) == 1:  # если ответов нет или он только один
                # (в чем смысл выбирать из одного ответа?)
                is_completable = False
                continue
        if row['taskType'] == 'textWithGaps':  # преобразуем текст с пропусками в нужный формат
            # функциональность текста с пропусками реализована только частично. Эта часть кода будет TODO
            testjson['task'][index]['content'] = [testjson['task'][index]['content']]
    print(testjson['task'])
    if test.user_id == current_user.id:
        test.task = json.dumps(testjson['task'])
        test.answers = json.dumps(testjson['answers'])
        test.scores = json.dumps(testjson['scores'])
        test.is_completable = is_completable
        db_sess.commit()
    return 'ok'


@app.route('/schoolar')
@login_required
def schoolar():  # cтраница ученика
    if current_user.status != 0:
        return redirect("/panel")
    db_sess = db.db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    classes = user.classes  # классы в которых находится ученик
    return render_template('schoolar.html', classes=classes)


@app.route('/test/save', methods=['POST'])
@login_required
def save_test_answers():  # cохранение ответов на тест
    testjson = request.json
    print(testjson)
    if current_user.status != 0:
        return redirect("/panel")
    db_sess = db.db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == testjson['testid']).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    canaccess = False
    for i in user.classes:  # проверяем, есть ли у ученика доступ к тесту
        for j in i.tests:
            if test.id == j.id:
                canaccess = True
                break
    if not canaccess:
        return redirect('/schoolar')
    score = 0
    maxscore = 0
    ans = testjson['answers']  # ответы ученика
    correct = json.loads(test.answers)  # обьект с правильными ответами
    scores = json.loads(test.scores)  # обьект с значениями очков за каждое задание
    for i in scores.values():
        maxscore += int(i)  # максимальное значение очков
    for i in correct.keys():
        print(correct[i])
        if type(correct[i]) == list:  # обработка нескольких ответов
            if i in ans:  # проверяем есть ли вообще ответ на это задание у ученика
                if sorted(ans[i]) == sorted(correct[i]):
                    score += int(scores[i])
        elif type(correct[i]) == str or type(correct[i]) == int:  # обработка одного ответа
            if i in ans:  # проверяем есть ли вообще ответ на это задание у ученика
                print("===========")
                print(ans[i])
                print(correct[i])
                print("===========")
                if ans[i] == correct[i]:
                    score += int(scores[i])
    query = db_sess.query(UserAnswer).filter(UserAnswer.user_id == current_user.id).filter(
        UserAnswer.test_id == testjson[
            'testid']).first()  # делаем запрос и проверяем, есть ли ответ от этого ученика для этого теста в базе данных
    if not query:  # если ответа еще нет в базе данных
        user_answer = UserAnswer()
        user_answer.answer = json.dumps(testjson['answers'])
        user_answer.completed = testjson['completed']
        user_answer.score = score
        user_answer.maxscore = maxscore
        user_answer.user_id = current_user.id
        user_answer.test_id = testjson['testid']
        user_answer.class_id = testjson['classid']
        db_sess.add(user_answer)
        db_sess.commit()
    else:  # если есть то просто редактируем
        query.answer = json.dumps(testjson['answers'])
        query.score = score
        query.maxscore = maxscore
        query.completed = testjson['completed']
        db_sess.commit()
    return ''


@app.route('/test/<int:classid>/<int:id>')  # classid чтобы знать, для какого именно класса мы проходим тест
def test(classid, id):  # cтраница с выполнением теста
    if current_user.status != 0:
        return redirect("/panel")
    db_sess = db.db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == id).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    usertest = db_sess.query(UserAnswer).filter(UserAnswer.user_id == current_user.id).filter(
        UserAnswer.class_id == classid).filter(UserAnswer.test_id == test.id).first()
    useranswers = {}
    if usertest:
        if usertest.completed == 1:
            return 'Вы уже проходили этот тест!'
        useranswers = json.loads(usertest.answer)
    canaccess = False
    for i in user.classes:  # проверяем, есть ли у ученика доступ к тесту
        for j in i.tests:
            if test.id == j.id:
                canaccess = True
                break
    if not canaccess:
        return redirect('/schoolar')
    return render_template('task.html', task=json.loads(test.task), testid=id, classid=classid, useranswers=useranswers)


@app.route('/invitation/<link>')
def accept_invitation(link):  # добавление ученика в класс по приглашению
    if current_user.status != 0:
        return redirect("/panel")
    db_sess = db.db_session.create_session()
    class_ = db_sess.query(Class).filter(Class.invitation_link == link).first()
    class_.users.append(db_sess.query(User).filter(User.id == current_user.id).first())
    db_sess.commit()
    return redirect("/schoolar")


@app.route('/panel/class/<int:classid>/schoolar/<int:userid>')
def check_schoolar_answers(classid, userid):  # показываем ответы ученика на все тесты в классе
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    class_ = db_sess.query(Class).filter(Class.user_id == classid).first()
    user = db_sess.query(User).filter(User.id == userid).first()
    tests = db_sess.query(UserAnswer).filter(UserAnswer.user_id == userid).filter(UserAnswer.class_id == classid).all()[
            ::-1]  # разворачиваем массив чтобы сверху показывались самые последние прохождения
    return render_template('answerspage.html', tests=tests, user=user, class_=class_)


@app.route('/deleteuserfromclass/<int:classid>/<int:userid>')
def deleteuserfromclass(classid, userid):  # удаление ученика из класса
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    class_ = db_sess.query(Class).filter(Class.id == classid).first()
    user = db_sess.query(User).filter(User.id == userid).first()
    if class_.user_id == current_user.id:  # проверяем что класс принадлежит залогиненному юзеру
        if user in class_.users:  # проверям что ученик действительно есть в классе
            class_.users.remove(user)
            db_sess.commit()
    return redirect('/panel/class/' + str(classid))


@app.route('/deletetask/<int:id>')
def deletetask(id):
    if current_user.status != 1:
        return redirect("/schoolar")
    db_sess = db.db_session.create_session()
    test = db_sess.query(Test).filter(Test.id == id).first()
    if test.user_id == current_user.id:
        db_sess.delete(test)
        db_sess.commit()
    return redirect('/panel/tests')


@app.route('/deleteclass/<int:id>')
def deleteclass(id):  # удаление класса
    db_sess = db.db_session.create_session()
    class_ = db_sess.query(Class).filter(Class.id == id).first()
    if class_.user_id == current_user.id:
        if len(class_.users) != 0:  # В классе не должно быть учеников при удалении.
            # Так как удаление класса это событие масштабное, чтобы полностью предотвратить возможность
            # случайного нажатия(учитель может случайно подумать что удаляет ученика из класса,
            # а на самом деле удаляет сам класс), сервер будет удалять класс только при условии,
            # что в нем нет учеников.
            return redirect(
                '/panel/classes?error=Нельзя удалить класс, пока в нем есть ученики. Удалите всех учеников из класса, а после удалите сам класс.')
        db_sess.delete(class_)
        db_sess.commit()
    return redirect('/panel/classes')


if __name__ == "__main__":
    app.run(debug=True)
