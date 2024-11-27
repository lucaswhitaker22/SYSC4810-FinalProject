from flask import Blueprint, jsonify, request
from datetime import datetime
import re
from problem2 import PasswordManager
class EnrollmentSystem:
    def __init__(self):
        self.password_checker = PasswordChecker()
        self.password_manager = PasswordManager()

    def enroll_user(self, username, password, role):
        """
        Enroll a new user in the system
        Returns (success, result) tuple where result is either user data or error messages
        """
        # Validate username format
        if not self._validate_username(username):
            return False, ["Invalid username format - must be a valid email address"]
            
        # Check password strength
        password_errors = self.password_checker.check_password(password, username)
        if password_errors:
            return False, password_errors
            
        # If validation passes, create user record
        if self.password_manager.add_user(username, password, role):
            return True, {
                'username': username,
                'role': role,
                'created_at': datetime.now().isoformat()
            }
        else:
            return False, ["Failed to add user to password file"]
        
    def _validate_username(self, username):
        """Validate username is in email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, username))

class PasswordChecker:
    def __init__(self):
        self.min_length = 8
        self.max_length = 12
        self.common_passwords = self._load_common_passwords()
        self.forbidden_words = {'password', 'admin', 'letmein', 'welcome'}
        
    def check_password(self, password, username):
        errors = []
        
        # Length checks (8-12 characters as per requirements)
        if len(password) < 8:
            errors.append(f"Password must be at least 8 characters")
        if len(password) > 12:
            errors.append(f"Password must be at most 12 characters")
        
        # Character type checks
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        if not re.search(r'[!@#$%*&]', password):
            errors.append("Password must contain at least one special character (!@#$%*&)")
        
        # Username check
        username_parts = username.lower().split('@')[0]
        if username_parts in password.lower():
            errors.append("Password cannot contain username")
            
        # Check for forbidden words
        password_lower = password.lower()
        for word in self.forbidden_words:
            if word in password_lower:
                errors.append(f"Password cannot contain the word '{word}'")
                break
            
        # Common password check
        if password.lower() in self.common_passwords:
            errors.append("Password is too common")
            
        return errors
        
    def _load_common_passwords(self):
        return {
            'password123',
            'admin123',
            'letmein',
            '12345678',
            'qwerty123',
            'welcome123',
            'password1',
            'abc123',
            '123456789',
            '1q2w3e4r'
        }

# Flask Blueprint for enrollment endpoints
bp = Blueprint('enrollment', __name__, url_prefix='/api/enroll')

@bp.route('/', methods=['POST'])
def enroll():
    data = request.get_json()
    required_fields = ['username', 'password', 'role']
    
    if not all(field in data for field in required_fields):
        return jsonify({
            'success': False,
            'error': 'Missing required fields'
        }), 400
        
    enrollment = EnrollmentSystem()
    success, result = enrollment.enroll_user(
        data['username'],
        data['password'],
        data['role']
    )
    
    if not success:
        return jsonify({
            'success': False,
            'errors': result
        }), 400
        
    return jsonify({
        'success': True,
        'message': 'User enrolled successfully',
        'user': result
    }), 201


import unittest

class TestEnrollment(unittest.TestCase):
    def setUp(self):
        self.enrollment = EnrollmentSystem()
        
    def test_valid_enrollment(self):
        """Test enrollment with valid credentials"""
        success, result = self.enrollment.enroll_user(
            "test@example.com",
            "ValidP@ss123",
            "CLIENT"
        )
        self.assertTrue(success)
        self.assertEqual(result['username'], "test@example.com")
        self.assertEqual(result['role'], "CLIENT")
        
    def test_password_validation(self):
        """Test password validation rules"""
        test_cases = [
            ("short1!", "test@example.com", False),  # Too short
            ("TooLongPass123!", "test@example.com", False),  # Too long
            ("nodigits!", "test@example.com", False),  # No digits
            ("NOLOWER1!", "test@example.com", False),  # No lowercase
            ("nouppercase1!", "test@example.com", False),  # No uppercase
            ("NoSpecial123", "test@example.com", False),  # No special chars
            ("Valid@P1", "test@example.com", True),  # Valid password
            ("test@Pass1!", "test@example.com", False),  # Contains username
            ("Password123!", "test@example.com", False)  # Common password
        ]
        
        for password, username, expected_valid in test_cases:
            success, errors = self.enrollment.enroll_user(username, password, "CLIENT")
            self.assertEqual(success, expected_valid, 
                f"Failed for password: {password}, expected: {expected_valid}, got: {success}")
    
    def test_username_validation(self):
        """Test username format validation"""
        invalid_usernames = [
            "notanemail",
            "missing@domain",
            "@nodomain.com",
            "spaces @domain.com",
            "symbols#@domain.com"
        ]
        
        for username in invalid_usernames:
            success, _ = self.enrollment.enroll_user(
                username,
                "ValidP@ss123",
                "CLIENT"
            )
            self.assertFalse(success)
            
    def test_common_password_check(self):
        """Test common password rejection"""
        success, errors = self.enrollment.enroll_user(
            "test@example.com",
            "password123",
            "CLIENT"
        )
        self.assertFalse(success)
        self.assertTrue(any("common" in error.lower() for error in errors))

if __name__ == '__main__':
    unittest.main()