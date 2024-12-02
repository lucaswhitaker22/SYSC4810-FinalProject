import os
import sys

# Add the problem directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'problems')))

from p1.main import AccessControl, Operation, Role
from p2.main import PasswordManager
from p3.main import UserEnrollment
from p4.main import UserLogin

def display_menu():
    print("\n=== justInvest System Prototype ===")
    print("1. Enroll a new user")
    print("2. Login")
    print("3. Exit")
    return input("Select an option (1-3): ")

def main():
    user_enrollment = UserEnrollment()
    user_login = UserLogin()

    while True:
        choice = display_menu()

        if choice == '1':
            user_enrollment.enroll_user()
        elif choice == '2':
            user_login.login_interface()
        elif choice == '3':
            print("Thank you for using justInvest. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()