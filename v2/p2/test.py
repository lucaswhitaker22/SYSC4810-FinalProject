import unittest
import os
import json
from main import PasswordManager, Role

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.pm = PasswordManager("test_passwd.txt")
        
    def tearDown(self):
        try:
            os.remove("test_passwd.txt")
        except FileNotFoundError:
            pass

    def test_password_file_creation(self):
        """Test password file is created properly"""
        self.assertTrue(os.path.exists("test_passwd.txt"))
        
        # Test file creation with custom path
        custom_pm = PasswordManager("custom_test.txt")
        self.assertTrue(os.path.exists("custom_test.txt"))
        os.remove("custom_test.txt")

    def test_salt_generation(self):
        """Test salt generation"""
        salt1 = self.pm._generate_salt()
        salt2 = self.pm._generate_salt()
        
        self.assertEqual(len(salt1), self.pm.SALT_LENGTH)
        self.assertNotEqual(salt1, salt2)

    def test_password_hashing(self):
        """Test password hashing consistency"""
        password = "TestPass123!"
        salt = self.pm._generate_salt()
        
        hash1 = self.pm._hash_password(password, salt)
        hash2 = self.pm._hash_password(password, salt)
        
        self.assertEqual(hash1, hash2)
        
        # Different passwords should produce different hashes
        hash3 = self.pm._hash_password("DifferentPass123!", salt)
        self.assertNotEqual(hash1, hash3)

    def test_user_management(self):
        """Test user addition and verification"""
        # Test successful user addition
        self.assertTrue(self.pm.add_user("testuser", "Password123!", Role.CLIENT))
        
        # Test duplicate username
        self.assertFalse(self.pm.add_user("testuser", "DiffPassword123!", Role.CLIENT))
        
        # Test empty username
        self.assertFalse(self.pm.add_user("", "Password123!", Role.CLIENT))
        
        # Test empty password
        self.assertFalse(self.pm.add_user("newuser", "", Role.CLIENT))
        

    def test_user_verification(self):
        """Test user verification scenarios"""
        # Add test user
        self.pm.add_user("verifyuser", "TestPass123!", Role.FINANCIAL_ADVISOR)
        
        # Test correct credentials
        success, role = self.pm.verify_user("verifyuser", "TestPass123!")
        self.assertTrue(success)
        self.assertEqual(role, Role.FINANCIAL_ADVISOR)
        
        # Test case sensitivity
        success, role = self.pm.verify_user("VERIFYUSER", "TestPass123!")
        self.assertFalse(success)
        
        # Test wrong password
        success, role = self.pm.verify_user("verifyuser", "WrongPass123!")
        self.assertFalse(success)
        self.assertIsNone(role)
        
        # Test empty credentials
        success, role = self.pm.verify_user("", "TestPass123!")
        self.assertFalse(success)
        success, role = self.pm.verify_user("verifyuser", "")
        self.assertFalse(success)
        

    def test_file_integrity(self):
        """Test password file integrity"""
        # Add test users
        test_users = [
            ("user1", "Pass123!", Role.CLIENT),
            ("user2", "Pass456!", Role.PREMIUM_CLIENT)
        ]
        
        for username, password, role in test_users:
            self.pm.add_user(username, password, role)
        
        # Verify file content structure
        with open("test_passwd.txt", 'r') as f:
            records = [json.loads(line.strip()) for line in f if line.strip()]
            
        self.assertEqual(len(records), len(test_users))
        for record in records:
            self.assertIn("username", record)
            self.assertIn("salt", record)
            self.assertIn("hash", record)
            self.assertIn("role", record)

    def test_concurrent_access(self):
        """Test multiple instances accessing the same file"""
        pm1 = PasswordManager("test_passwd.txt")
        pm2 = PasswordManager("test_passwd.txt")
        
        pm1.add_user("user1", "Pass123!", Role.CLIENT)
        success, role = pm2.verify_user("user1", "Pass123!")
        self.assertTrue(success)
        self.assertEqual(role, Role.CLIENT)

if __name__ == '__main__':
    unittest.main()