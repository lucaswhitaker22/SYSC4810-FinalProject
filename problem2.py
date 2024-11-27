from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
import json
from datetime import datetime
import secrets

class PasswordManager:
    def __init__(self, file_path='passwd.txt'):
        self.file_path = file_path
        self.ph = PasswordHasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            salt_len=16
        )
    
    def add_user(self, username, password, role):
        """Add a new user to the password file"""
        try:
            # Generate hash
            hash = self.ph.hash(password)
            
            # Create user record
            user_record = {
                'username': username,
                'hash': hash,
                'role': role,
                'created_at': int(datetime.now().timestamp()),
                'last_login': None
            }
            
            # Append to file
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(user_record) + '\n')
            
            return True
        except Exception as e:
            print(f"Error adding user: {str(e)}")
            return False
    
    def verify_user(self, username, password):
        """Verify user credentials and update last login"""
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                record = json.loads(line)
                if record['username'] == username:
                    try:
                        # Verify password
                        self.ph.verify(record['hash'], password)
                        
                        # Update last login
                        record['last_login'] = int(datetime.now().timestamp())
                        lines[i] = json.dumps(record) + '\n'
                        
                        # Write updated records back to file
                        with open(self.file_path, 'w') as f:
                            f.writelines(lines)
                        
                        return record['role']
                    except VerifyMismatchError:
                        return None
            
            return None
        except Exception as e:
            print(f"Error verifying user: {str(e)}")
            return None
        
import unittest

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.test_file = 'test_passwd.txt'
        self.pm = PasswordManager(self.test_file)
        
    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_user(self):
        """Test user addition functionality"""
        # Test successful user addition
        result = self.pm.add_user('test@example.com', 'SecurePass123!', 'CLIENT')
        self.assertTrue(result)
        
        # Verify file exists and contains correct record
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            record = json.loads(f.readline())
            self.assertEqual(record['username'], 'test@example.com')
            self.assertEqual(record['role'], 'CLIENT')
            self.assertIsNotNone(record['hash'])
            self.assertIsNotNone(record['created_at'])
            self.assertIsNone(record['last_login'])
    
    def test_verify_user(self):
        """Test user verification functionality"""
        # Add test user
        self.pm.add_user('alice@example.com', 'TestPass456!', 'PREMIUM_CLIENT')
        
        # Test successful verification
        role = self.pm.verify_user('alice@example.com', 'TestPass456!')
        self.assertEqual(role, 'PREMIUM_CLIENT')
        
        # Verify last_login was updated
        with open(self.test_file, 'r') as f:
            record = json.loads(f.readline())
            self.assertIsNotNone(record['last_login'])
    
    def test_failed_verification(self):
        """Test failed verification attempts"""
        # Add test user
        self.pm.add_user('bob@example.com', 'StrongPass789!', 'FINANCIAL_ADVISOR')
        
        # Test wrong password
        role = self.pm.verify_user('bob@example.com', 'WrongPass123!')
        self.assertIsNone(role)
        
        # Test non-existent user
        role = self.pm.verify_user('nonexistent@example.com', 'AnyPass123!')
        self.assertIsNone(role)
    
    def test_multiple_users(self):
        """Test handling multiple users"""
        # Add multiple users
        users = [
            ('user1@example.com', 'Pass123!', 'CLIENT'),
            ('user2@example.com', 'Pass456!', 'PREMIUM_CLIENT'),
            ('user3@example.com', 'Pass789!', 'FINANCIAL_ADVISOR')
        ]
        
        for username, password, role in users:
            self.pm.add_user(username, password, role)
        
        # Verify each user
        for username, password, expected_role in users:
            role = self.pm.verify_user(username, password)
            self.assertEqual(role, expected_role)
    
    def test_password_hash_uniqueness(self):
        """Test that identical passwords generate different hashes"""
        # Add two users with same password
        self.pm.add_user('user1@example.com', 'SamePass123!', 'CLIENT')
        self.pm.add_user('user2@example.com', 'SamePass123!', 'CLIENT')
        
        # Read hashes
        with open(self.test_file, 'r') as f:
            records = [json.loads(line) for line in f]
        
        # Verify hashes are different
        self.assertNotEqual(records[0]['hash'], records[1]['hash'])

if __name__ == '__main__':
    unittest.main()