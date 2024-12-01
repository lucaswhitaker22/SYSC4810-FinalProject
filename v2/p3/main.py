import re
from typing import Tuple, Optional
from enum import Enum

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:/Users/lucas/git/SYSC4810/SYSC4810-FinalProject/v2')
from p1.main import Role
from p2.main import PasswordManager

class PasswordChecker:
    def __init__(self, weak_passwords_file: str = "weak_passwords.txt"):
        self.weak_passwords_file = weak_passwords_file
        self.weak_passwords = self._load_weak_passwords()
        self.special_chars = {'!', '@', '#', '$', '%', '*', '&'}

    def _load_weak_passwords(self) -> set:
        try:
            with open(self.weak_passwords_file, 'r') as f:
                return set(line.strip().lower() for line in f)
        except FileNotFoundError:
            return set()

    def check_password(self, password: str, username: str) -> Tuple[bool, Optional[str]]:
        if len(password) < 8 or len(password) > 12:
            return False, "Password must be between 8 and 12 characters"
                
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
                
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
                
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
                
        if not any(c in self.special_chars for c in password):
            return False, "Password must contain at least one special character (!@#$%*&)"
                
        # Check username in password (case-insensitive)
        username_lower = username.lower()
        password_lower = password.lower()
        if username_lower in password_lower:
            return False, "Password cannot contain username"
                
        if password.lower() in self.weak_passwords:
            return False, "Password is too common"
                
        return True, None

class UserEnrollment:
    def __init__(self):
        self.password_checker = PasswordChecker()
        self.password_manager = PasswordManager()

    def enroll_user(self) -> bool:
        print("\n=== justInvest User Enrollment ===")
        
        # Get username
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty")
            return False

        # Get role
        print("\nAvailable roles:")
        for role in Role:
            print(f"- {role.value}")
        role_input = input("Enter role: ").strip()
        try:
            role = Role(role_input)
        except ValueError:
            print("Invalid role selected")
            return False

        # Get and validate password
        while True:
            password = input("Enter password: ")
            valid, message = self.password_checker.check_password(password, username)
            
            if valid:
                # Confirm password
                confirm = input("Confirm password: ")
                if password != confirm:
                    print("Passwords do not match")
                    continue
                break
            else:
                print(f"Invalid password: {message}")

        # Add user to password file
        if self.password_manager.add_user(username, password, role):
            print("User successfully enrolled!")
            return True
        else:
            print("Failed to enroll user. Username may already exist.")
            return False