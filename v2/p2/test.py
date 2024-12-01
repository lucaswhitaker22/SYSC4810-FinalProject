import unittest
from main import PasswordManager, Role

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.pm = PasswordManager("test_passwd.txt")
        
    def tearDown(self):
        import os
        try:
            os.remove("test_passwd.txt")
        except FileNotFoundError:
            pass

    def test_add_user(self):
        # Test adding new user
        self.assertTrue(self.pm.add_user("testuser", "Password123!", Role.CLIENT))
        
        # Test duplicate username
        self.assertFalse(self.pm.add_user("testuser", "DiffPassword123!", Role.CLIENT))

    def test_verify_user(self):
        # Add test user
        self.pm.add_user("verifyuser", "TestPass123!", Role.FINANCIAL_ADVISOR)
        
        # Test correct credentials
        success, role = self.pm.verify_user("verifyuser", "TestPass123!")
        self.assertTrue(success)
        self.assertEqual(role, Role.FINANCIAL_ADVISOR)
        
        # Test wrong password
        success, role = self.pm.verify_user("verifyuser", "WrongPass123!")
        self.assertFalse(success)
        self.assertIsNone(role)
        
        # Test non-existent user
        success, role = self.pm.verify_user("nonexistent", "Password123!")
        self.assertFalse(success)
        self.assertIsNone(role)

    def test_multiple_users(self):
        # Add multiple users
        test_users = [
            ("sasha.kim", "SashaPass123!", Role.CLIENT),
            ("noor.abbasi", "NoorPass123!", Role.PREMIUM_CLIENT),
            ("mikael.chen", "MikaelPass123!", Role.FINANCIAL_ADVISOR)
        ]
        
        for username, password, role in test_users:
            self.assertTrue(self.pm.add_user(username, password, role))
            
        # Verify each user
        for username, password, role in test_users:
            success, verified_role = self.pm.verify_user(username, password)
            self.assertTrue(success)
            self.assertEqual(verified_role, role)

if __name__ == '__main__':
    unittest.main()