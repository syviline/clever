from flask import Flask
from sqlalchemy import exists

from data import db_session
from data.users import User
from data.classes import Class
from data.tests import Test
import datetime

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_GGD'
ERR_EMAIL = -10
OUT_SUCCESS = 1


def add_user(db_sess, **qwargs) -> User:
    email = qwargs.get("email").lower()
    if email is None or email_exists(db_sess, email):
        return ERR_EMAIL
    # db_sess = db_session.create_session()
    user = User()
    user.name = qwargs.get("name")
    user.surname = qwargs.get("surname")
    user.email = email
    user.set_password(qwargs.get('password'))
    user.status = qwargs.get("status")

    db_sess.add(user)
    db_sess.commit()
    return User


def all_users():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)


def create_class(db_sess, **qwargs) -> Class:
    obj = Class()
    obj.title = qwargs.get("title")
    # obj.user_id = qwargs.get("user_id")
    obj.user = qwargs.get("user")
    obj.is_private = qwargs.get("is_private")
    obj.users = qwargs.get("users")
    db_sess.add(obj)
    db_sess.commit()
    return obj


def create_test(db_sess, **qwargs) -> Test:
    obj = Test()

    obj.title = qwargs.get("title")
    # obj.user_id = qwargs.get("user_id")
    obj.user = qwargs.get("user")
    obj.task = qwargs.get("task")
    obj.is_private = qwargs.get("is_private")
    obj.users = qwargs.get("users")
    obj.classes = qwargs.get("classes")
    db_sess.add(obj)
    db_sess.commit()
    return obj


def email_exists(db_sess, email: str) -> bool:
    # db_sess = db_session.create_session()
    is_exists = db_sess.query(exists().where(User.email == email.lower())).scalar()
    return is_exists


def test_user_exists(db_sess, test_id, user_id) -> bool:
    # db_sess = db_session.create_session()
    is_exists = db_sess.query(exists().where((Test.id == test_id) & (Test.user_id == user_id))).scalar()
    return is_exists


def db_ex(commit=True):
    # addUser()
    db_sess = db_session.create_session()
    #
    print("===")
    user1 = add_user(db_sess, email="ivan@mail.ru", hashed_password="qwertyuiop[-=0", name="Ivan", surname="Ivanov")
    user2 = add_user(db_sess, email="ivan2@mail.ru", hashed_password="sdffesdfa1342", name="Ivan2", surname="Ivanov2")
    user3 = add_user(db_sess, email="ivan3@mail.ru", hashed_password="gffjy0--=372d", name="Ivan3", surname="Ivanov3")
    print("addUser", )
    #
    print("===")
    user = db_sess.query(User).first()
    print(user.name)
    #
    print("===")
    for user in db_sess.query(User).all():
        print(user)
    #
    print("===")
    db_sess.delete(user)
    if commit:
        db_sess.commit()
    #
    # for user in db_sess.query(User).filter((User.id > 1) | (User.email.notilike("%1%"))):
    #     print(user)
    # #
    # print("===")
    # user = db_sess.query(User).filter(User.id == 1).first()
    # print(user)
    # user.name = "Измененное имя пользователя"
    # user.created_date = datetime.datetime.now()
    # db_sess.commit()
    # #
    # print("===")
    # db_sess.query(User).delete()
    # db_sess.commit()
    # #
    # print("===")
    # user = db_sess.query(User).filter(User.id == 2).first()
    # db_sess.delete(user)
    # db_sess.commit()
    # #
    # print("===")
    # # news = News(title="Первая новость", content="Привет блог!",
    # #             user_id=1, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()
    #
    # print("===")
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Вторая новость", content="Уже вторая запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()
    # #
    # print("===")
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Личная запись", content="Эта запись личная",
    #             is_private=True)
    # user.news.append(news)
    # db_sess.commit()
    # #
    # print("===")
    # for news in user.news:
    #     print(news)


def main():
    db_session.global_init("db/clever.db")
    db_ex(commit=False)
    db_ex()

    # app.run()


if __name__ == '__main__':
    main()
