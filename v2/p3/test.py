import unittest
from unittest.mock import patch
import os
from main import PasswordChecker, UserEnrollment, Role

class TestUserEnrollment(unittest.TestCase):
    def setUp(self):
        self.password_checker = PasswordChecker()
        self.enrollment = UserEnrollment()
        # Create weak passwords file
        with open("weak_passwords.txt", "w") as f:
            f.write("password123\nqwerty123\nadmin123\n")
        
    def tearDown(self):
        # Clean up test files
        for file in ["passwd.txt", "weak_passwords.txt"]:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    def test_password_validation_length(self):
        """Test password length requirements"""
        test_cases = [
            ("Short1!", False),
            ("VeryLongPass123!", False),
            ("Valid123!", True)
        ]
        for password, expected in test_cases:
            valid, _ = self.password_checker.check_password(password, "user")
            self.assertEqual(valid, expected)
    def test_password_username_match(self):
        """Test username matching prevention"""
        username = "testuser"
        test_cases = [
            # Format: (password, expected_valid, description)
            ("testuser123!", False, "Contains exact username"),
            ("TestUser123!", False, "Contains username with different case"),
            ("test123user!", False, "Contains username split"),
            ("Secure123!@", True, "Valid password without username"),
            ("Testing123!", True, "Valid password with partial match")
        ]
        
        for password, expected_valid, description in test_cases:
            valid, message = self.password_checker.check_password(password, username)
            self.assertEqual(
                valid, 
                expected_valid, 
                f"{description}: Password '{password}' with username '{username}'. Message: {message}"
            )

    def test_weak_password_check(self):
        """Test weak password detection"""
        test_cases = [
            ("password123", False),
            ("qwerty123", False),
            ("Unique123!", True)
        ]
        for password, expected in test_cases:
            valid, _ = self.password_checker.check_password(password.capitalize(), "user")
            self.assertEqual(valid, expected)

    @patch('builtins.input')
    def test_successful_enrollment(self, mock_input):
        mock_inputs = ['newuser', 'Client', 'Test123!@', 'Test123!@']
        mock_input.side_effect = mock_inputs
        result = self.enrollment.enroll_user()
        self.assertTrue(result)

    @patch('builtins.input')
    def test_duplicate_enrollment(self, mock_input):
        # First enrollment
        mock_inputs1 = ['testuser', 'Client', 'Test123!@', 'Test123!@']
        mock_input.side_effect = mock_inputs1
        self.enrollment.enroll_user()
        
        # Second enrollment attempt
        mock_inputs2 = ['testuser', 'Client', 'Test123!@', 'Test123!@']
        mock_input.side_effect = mock_inputs2
        result = self.enrollment.enroll_user()
        self.assertFalse(result)

    @patch('builtins.input')
    def test_enrollment_validation(self, mock_input):
        test_cases = [
            (['', 'Client', 'Pass123!@', 'Pass123!@'], False),
            (['user', 'Invalid', 'Pass123!@', 'Pass123!@'], False),
            (['user', 'Client', 'weak', 'weak', 'Pass123!@', 'Pass123!@'], True)
        ]
        
        for inputs, expected in test_cases:
            mock_input.side_effect = inputs
            result = self.enrollment.enroll_user()
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()