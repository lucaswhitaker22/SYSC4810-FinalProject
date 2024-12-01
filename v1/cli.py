from problem2 import PasswordManager
from problem1 import AccessControl, Role, Permission
from problem3 import EnrollmentSystem
import cmd

class JustInvestCLI(cmd.Cmd):
    prompt = 'justInvest> '

    def __init__(self):
        super().__init__()
        self.password_manager = PasswordManager()
        self.access_control = AccessControl()
        self.enrollment_system = EnrollmentSystem()
        self.current_user = None

    def do_enroll(self, arg):
        """Enroll a new user: enroll <username> <password> <role>"""
        args = arg.split()
        if len(args) != 3:
            print("Usage: enroll <username> <password> <role>")
            return

        username, password, role = args
        success, result = self.enrollment_system.enroll_user(username, password, role)
        if success:
            print(f"User {username} enrolled successfully as {role}.")
        else:
            print("Enrollment failed:")
            for error in result:
                print(f"- {error}")

    def do_login(self, arg):
        """Login to the system: login <username> <password>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: login <username> <password>")
            return

        username, password = args
        role = self.password_manager.verify_user(username, password)
        if role:
            self.current_user = {'username': username, 'role': role}
            print(f"Login successful. Welcome, {username}!")
        else:
            print("Invalid credentials. Please try again.")

    def do_logout(self, arg):
        """Logout from the system"""
        if self.current_user:
            self.current_user = None
            print("Logout successful.")
        else:
            print("You are not logged in.")

    def do_info(self, arg):
        """Display user information and permissions"""
        if not self.current_user:
            print("You are not logged in.")
            return

        username = self.current_user['username']
        role = Role[self.current_user['role']]
        permissions = self.access_control.get_user_permissions(role)

        print(f"\nUser Information:")
        print(f"Username: {username}")
        print(f"Role: {role.name}")
        print("\nAvailable Operations:")
        for perm in permissions:
            print(f"- {perm.name.replace('_', ' ').title()}")

    def do_quit(self, arg):
        """Quit the application"""
        print("Thank you for using justInvest. Goodbye!")
        return True

if __name__ == '__main__':
    JustInvestCLI().cmdloop()