import unittest
from unittest.mock import patch
from main import PasswordChecker, UserEnrollment

class TestUserEnrollment(unittest.TestCase):
    def setUp(self):
        self.password_checker = PasswordChecker()
        self.enrollment = UserEnrollment()

    def test_password_validation(self):
        # Test password length (too short)
        valid, _ = self.password_checker.check_password("Abc1!", "user")
        self.assertFalse(valid)

        # Test password length (too long)
        valid, _ = self.password_checker.check_password("Abcd1234!@#$%", "user")
        self.assertFalse(valid)

        # Test uppercase requirement
        valid, _ = self.password_checker.check_password("abcd123!", "user")
        self.assertFalse(valid)

        # Test lowercase requirement
        valid, _ = self.password_checker.check_password("ABCD123!", "user")
        self.assertFalse(valid)

        # Test digit requirement
        valid, _ = self.password_checker.check_password("AbcdEfg!", "user")
        self.assertFalse(valid)

        # Test special character requirement
        valid, _ = self.password_checker.check_password("Abcd1234", "user")
        self.assertFalse(valid)

        # Test username matching
        valid, _ = self.password_checker.check_password("user123!", "user")
        self.assertFalse(valid)

        # Test valid password
        valid, _ = self.password_checker.check_password("Test123!@", "user")
        self.assertTrue(valid)

    
    @patch('builtins.input')
    def test_successful_enrollment(self, mock_input):
        # Create a new mock input sequence with proper role value
        mock_input.side_effect = [
            'testuser',           # username
            'Client',            # exact role value from enum
            'Test123!@',         # initial password
            'Test123!@'          # password confirmation
        ]
        
        # Clean up any existing password file before test
        import os
        if os.path.exists("passwd.txt"):
            os.remove("passwd.txt")
            
        result = self.enrollment.enroll_user()
        self.assertTrue(result)

    @patch('builtins.input')
    def test_invalid_role_enrollment(self, mock_input):
        mock_input.side_effect = ['testuser', 'InvalidRole', 'Test123!@']
        result = self.enrollment.enroll_user()
        self.assertFalse(result)

    @patch('builtins.input')
    def test_weak_password_enrollment(self, mock_input):
        mock_input.side_effect = [
            'testuser2',          # username
            'Client',            # role
            'weak',              # first password attempt (weak)
            'Test123!@',         # second password attempt
            'Test123!@'          # password confirmation
        ]
        result = self.enrollment.enroll_user()
        self.assertTrue(result)
if __name__ == '__main__':
    unittest.main(failfast=True)