import unittest
from unittest.mock import patch, Mock
import os
from main import UserLogin, Role, Operation

class LoginTests(unittest.TestCase):
    def setUp(self):
        self.login = UserLogin()
        self.setup_test_users()
    
    def tearDown(self):
        if os.path.exists("passwd.txt"):
            os.remove("passwd.txt")
    
    def setup_test_users(self):
        test_data = [
            ("bob", "Test123!@", Role.CLIENT),
            ("alice", "Test123!@", Role.PREMIUM_CLIENT),
            ("charlie", "Test123!@", Role.FINANCIAL_ADVISOR),
            ("dave", "Test123!@", Role.FINANCIAL_PLANNER),
            ("eve", "Test123!@", Role.TELLER)
        ]
        
        for username, pwd, role in test_data:
            self.login.password_manager.add_user(username, pwd, role)

    def test_basic_login(self):
        tests = [
            ("bob", "Test123!@", True, Role.CLIENT),
            ("bob", "WrongPass!", False, None),
            ("nobody", "Test123!@", False, None),
            ("bob", "", False, None),
            ("", "Test123!@", False, None)
        ]
        
        for username, pwd, should_pass, expected_role in tests:
            with self.subTest(user=username):
                success, role = self.login.login(username, pwd)
                self.assertEqual(success, should_pass)
                self.assertEqual(role, expected_role)

    def test_permissions(self):
        expected = {
            Role.CLIENT: {
                Operation.VIEW_BALANCE,
                Operation.VIEW_PORTFOLIO,
                Operation.VIEW_FA_CONTACT
            },
            Role.PREMIUM_CLIENT: {
                Operation.VIEW_BALANCE,
                Operation.VIEW_PORTFOLIO,
                Operation.MODIFY_PORTFOLIO,
                Operation.VIEW_FP_CONTACT
            },
            Role.FINANCIAL_ADVISOR: {
                Operation.VIEW_BALANCE,
                Operation.VIEW_PORTFOLIO,
                Operation.MODIFY_PORTFOLIO,
                Operation.VIEW_PRIVATE_INSTRUMENTS
            },
            Role.FINANCIAL_PLANNER: {
                Operation.VIEW_BALANCE,
                Operation.VIEW_PORTFOLIO,
                Operation.MODIFY_PORTFOLIO,
                Operation.VIEW_MARKET_INSTRUMENTS,
                Operation.VIEW_PRIVATE_INSTRUMENTS
            },
            Role.TELLER: {
                Operation.VIEW_BALANCE,
                Operation.VIEW_PORTFOLIO
            }
        }
        
        for role, perms in expected.items():
            with self.subTest(role=role):
                actual = self.login.access_control.get_user_permissions(role)
                self.assertEqual(actual, perms)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_login_interface(self, mock_print, mock_input):
        tests = [
            (["bob", "Test123!@"], True),
            (["bob", "wrong"], False),
            (["", "Test123!@"], False),
            (["bob", ""], False),
            (["nobody", "Test123!@"], False)
        ]
        
        for inputs, expected in tests:
            with self.subTest(inputs=inputs):
                mock_input.side_effect = inputs
                result = self.login.login_interface()
                self.assertEqual(result, expected)

    @patch('builtins.print')
    def test_privilege_display(self, mock_print):
        test_users = [
            ("bob", Role.CLIENT),
            ("alice", Role.PREMIUM_CLIENT),
            ("charlie", Role.FINANCIAL_ADVISOR)
        ]
        
        for username, role in test_users:
            self.login.display_user_privileges(username, role)
            mock_print.assert_any_call(f"Username: {username}")
            mock_print.assert_any_call(f"Role: {role.value}")

    def test_multiple_logins(self):
        # First login
        ok1, role1 = self.login.login("bob", "Test123!@")
        self.assertTrue(ok1)
        self.assertEqual(role1, Role.CLIENT)
        
        # Second login
        ok2, role2 = self.login.login("alice", "Test123!@")
        self.assertTrue(ok2)
        self.assertEqual(role2, Role.PREMIUM_CLIENT)


if __name__ == '__main__':
    unittest.main()