import unittest
from unittest.mock import patch
from main import UserLogin, Role, Operation

class TestUserLogin(unittest.TestCase):
    def setUp(self):
        self.login_manager = UserLogin()
        # Add test user for login tests
        self.login_manager.password_manager.add_user(
            "testuser", "Test123!@", Role.CLIENT
        )

    def test_successful_login(self):
        success, role = self.login_manager.login("testuser", "Test123!@")
        self.assertTrue(success)
        self.assertEqual(role, Role.CLIENT)

    def test_failed_login_wrong_password(self):
        success, role = self.login_manager.login("testuser", "WrongPass123!")
        self.assertFalse(success)
        self.assertIsNone(role)

    def test_failed_login_nonexistent_user(self):
        success, role = self.login_manager.login("nonexistent", "Test123!@")
        self.assertFalse(success)
        self.assertIsNone(role)

    def test_client_privileges(self):
        self.login_manager.display_user_privileges("testuser", Role.CLIENT)
        permissions = self.login_manager.access_control.get_user_permissions(Role.CLIENT)
        self.assertIn(Operation.VIEW_BALANCE, permissions)
        self.assertIn(Operation.VIEW_PORTFOLIO, permissions)
        self.assertIn(Operation.VIEW_FA_CONTACT, permissions)

    @patch('builtins.input', side_effect=['testuser', 'Test123!@'])
    def test_login_interface_success(self, mock_input):
        result = self.login_manager.login_interface()
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['testuser', 'WrongPass'])
    def test_login_interface_failure(self, mock_input):
        result = self.login_manager.login_interface()
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['', 'Test123!@'])
    def test_login_interface_empty_username(self, mock_input):
        result = self.login_manager.login_interface()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()