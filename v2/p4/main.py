from typing import Optional, Tuple

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:/Users/lucas/git/SYSC4810/SYSC4810-FinalProject/v2')

from p2.main import PasswordManager
from p1.main import AccessControl,Role, Operation


class UserLogin:
    def __init__(self):
        self.password_manager = PasswordManager()
        self.access_control = AccessControl()

    def login(self, username: str, password: str) -> Tuple[bool, Optional[Role]]:
        """Verify user credentials and return role if valid"""
        return self.password_manager.verify_user(username, password)

    def display_user_privileges(self, username: str, role: Role):
        """Display user information and access privileges"""
        print(f"\n=== User Information ===")
        print(f"Username: {username}")
        print(f"Role: {role.value}")
        
        print("\nAccess Privileges:")
        permissions = self.access_control.get_user_permissions(role)
        for operation in sorted(permissions, key=lambda x: x.value):
            print(f"- {operation.value}")

    def login_interface(self) -> bool:
        """Display login interface and handle user authentication"""
        print("\n=== justInvest Login ===")
        
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty")
            return False
            
        password = input("Password: ").strip()
        if not password:
            print("Password cannot be empty")
            return False

        success, role = self.login(username, password)
        if success and role:
            print("\nLogin successful!")
            self.display_user_privileges(username, role)
            return True
        else:
            print("Invalid username or password")
            return False