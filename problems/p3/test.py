import unittest
from unittest.mock import patch
import os
from main import PasswordChecker, UserEnrollment, Role

class TestBase(unittest.TestCase):
    def setUp(self):
        self.setup_test_files()
    
    def tearDown(self):
        self.remove_test_files()
    
    def setup_test_files(self):
        with open("weak_passwords.txt", "w") as f:
            f.write("password123\nqwerty123\nadmin123")
    
    def remove_test_files(self):
        test_files = ["passwd.txt", "weak_passwords.txt"]
        for f in test_files:
            if os.path.exists(f):
                os.remove(f)


class PasswordTests(TestBase):
    def setUp(self):
        super().setUp()
        self.pwd_checker = PasswordChecker()

    def test_basic_requirements(self):
        passwords = [
            ("short!", False),
            ("waytoolongpassword123!", False), 
            ("GoodPass1!", True)
        ]
        
        for pwd, should_pass in passwords:
            with self.subTest(pwd=pwd):
                result, _ = self.pwd_checker.check_password(pwd, "someuser")
                self.assertEqual(result, should_pass)

    def test_username_checks(self):
        user = "bobsmith"
        tests = [
            ("bobsmith123!", False),
            ("BOBsmith456!", False),
            ("bob123smith!", False),
            ("GoodPass1!", True)
        ]
        
        for pwd, should_pass in tests:
            with self.subTest(pwd=pwd):
                result, _ = self.pwd_checker.check_password(pwd, user)
                self.assertEqual(result, should_pass)

    def test_weak_password_list(self):
        tests = [
            ("Password123", False),
            ("qwerty123", False),
            ("Str0ngP@ss!", True)
        ]
        
        for pwd, should_pass in tests:
            with self.subTest(pwd=pwd):
                result, _ = self.pwd_checker.check_password(pwd, "user")
                self.assertEqual(result, should_pass)


class EnrollmentTests(TestBase):
    def setUp(self):
        super().setUp()
        self.enroll = UserEnrollment()

    def try_enroll(self, inputs):
        with patch('builtins.input', side_effect=inputs):
            return self.enroll.enroll_user()

    def test_enrollment_flows(self):
        test_flows = {
            "happy_path": (
                ["jdoe", "Client", "GoodPass1!", "GoodPass1!"],
                True
            ),
            "blank_user": (
                ["", "Client", "GoodPass1!", "GoodPass1!"],
                False
            ),
            "bad_role": (
                ["jdoe", "BadRole", "GoodPass1!", "GoodPass1!"],
                False
            )
        }
        
        for name, (inputs, expected) in test_flows.items():
            with self.subTest(case=name):
                result = self.try_enroll(inputs)
                self.assertEqual(result, expected)

    def test_duplicate_users(self):
        # First signup
        self.try_enroll(["jsmith", "Client", "GoodPass1!", "GoodPass1!"])
        
        # Try duplicate
        result = self.try_enroll(["jsmith", "Client", "GoodPass1!", "GoodPass1!"])
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()