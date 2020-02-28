from app import db, bcrypt
from app.models import User
from getpass import getpass


def create_user():
    print("Creating new user...")
    user = User()
    print("Enter username: ", end="")
    user.username = input()
    print("Enter email: ", end="")
    user.email = input()
    print("Enter password: ", end="")
    user.password = getpass()
    assert user.password == getpass('Password (again):')

    user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')
    user.role = 0

    db.session.add(user)
    db.session.commit()

    print("\r\nAdded user.")


def main():
    if User.query.all():
        print('A user already exists! Create another? (y/n): ', end="")
        char = input()
        if char != 'y':
            print("Alright... Not creating another one.")
            return
        else:
            create_user()
    else:
        create_user()


if __name__ == "__main__":
    main()
