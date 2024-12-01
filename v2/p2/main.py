import hashlib
import os
import json
from typing import Optional, Dict, Tuple
from enum import Enum
import sys

sys.path.insert(1, "C:/Users/lucas/git/SYSC4810/SYSC4810-FinalProject/v2")

from p1.main import AccessControl, Operation, Role


class PasswordManager:
    def __init__(self, password_file: str = "passwd.txt"):
        self.password_file = password_file
        self.SALT_LENGTH = 32
        self.HASH_ITERATIONS = 100000
        # Ensure password file exists
        if not os.path.exists(password_file):
            open(password_file, "a").close()

    def _generate_salt(self) -> bytes:
        return os.urandom(self.SALT_LENGTH)

    def _hash_password(self, password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, self.HASH_ITERATIONS
        )

    def add_user(self, username: str, password: str, role: Role) -> bool:
        try:

            if username == "" or password == "":
                return False
            # Generate salt and hash password
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)

            # Create user record
            user_record = {
                "username": username,
                "salt": salt.hex(),
                "hash": password_hash.hex(),
                "role": role.value,
            }

            # Read existing records
            existing_records = []
            try:
                with open(self.password_file, "r") as f:
                    existing_records = [
                        json.loads(line.strip()) for line in f if line.strip()
                    ]
            except FileNotFoundError:
                pass

            # Check if username already exists
            if any(record["username"] == username for record in existing_records):
                return False

            # Append new record
            with open(self.password_file, "a") as f:
                f.write(json.dumps(user_record) + "\n")

            return True

        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def verify_user(self, username: str, password: str) -> Tuple[bool, Optional[Role]]:
        """Verify user credentials and return role if valid"""
        try:
            # Input validation
            if username is None or password is None:
                return False, None
                
            if not isinstance(username, str) or not isinstance(password, str):
                return False, None
                
            if not username.strip() or not password.strip():
                return False, None

            with open(self.password_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    if record["username"] == username:
                        salt = bytes.fromhex(record["salt"])
                        stored_hash = bytes.fromhex(record["hash"])
                        computed_hash = self._hash_password(password, salt)
                        
                        if computed_hash == stored_hash:
                            return True, Role(record["role"])
                        return False, None
                        
            return False, None
            
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False, None

