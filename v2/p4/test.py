import unittest
from unittest.mock import patch, Mock
import os
from main import UserLogin, Role, Operation

class TestUserLogin(unittest.TestCase):
    def setUp(self):
        """Initialize test environment with test users"""
        self.login_manager = UserLogin()
        
        # Create test users with different roles
        self.test_users = {
            "client_user": ("Test123!@", Role.CLIENT),
            "premium_user": ("Test123!@", Role.PREMIUM_CLIENT),
            "advisor_user": ("Test123!@", Role.FINANCIAL_ADVISOR),
            "planner_user": ("Test123!@", Role.FINANCIAL_PLANNER),
            "teller_user": ("Test123!@", Role.TELLER)
        }
        
        # Add test users to password file
        for username, (password, role) in self.test_users.items():
            self.login_manager.password_manager.add_user(username, password, role)

    def tearDown(self):
        """Clean up test environment"""
        try:
            os.remove("passwd.txt")
        except FileNotFoundError:
            pass

    def test_login_validation(self):
        """Test various login validation scenarios"""
        test_cases = [
            # (username, password, expected_success, expected_role, description)
            ("client_user", "Test123!@", True, Role.CLIENT, "Valid credentials"),
            ("client_user", "WrongPass123!", False, None, "Wrong password"),
            ("nonexistent", "Test123!@", False, None, "Non-existent user"),
            ("client_user", "", False, None, "Empty password"),
            ("", "Test123!@", False, None, "Empty username"),
            (None, "Test123!@", False, None, "None username"),
            ("client_user", None, False, None, "None password")
        ]
        
        for username, password, exp_success, exp_role, desc in test_cases:
            success, role = self.login_manager.login(username, password)
            self.assertEqual(success, exp_success, f"Failed case: {desc}")
            self.assertEqual(role, exp_role, f"Failed case: {desc}")

    def test_role_specific_permissions(self):
        """Test permissions for each role"""
        role_permissions = {
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
        
        for role, expected_permissions in role_permissions.items():
            permissions = self.login_manager.access_control.get_user_permissions(role)
            self.assertEqual(
                permissions, 
                expected_permissions,
                f"Incorrect permissions for role {role}"
            )

    @patch('builtins.input')
    @patch('builtins.print')
    def test_login_interface_scenarios(self, mock_print, mock_input):
        """Test various login interface scenarios"""
        test_cases = [
            # (inputs, expected_result, description)
            (
                ['client_user', 'Test123!@'],
                True,
                "Successful login"
            ),
            (
                ['client_user', 'WrongPass123!'],
                False,
                "Failed login - wrong password"
            ),
            (
                ['', 'Test123!@'],
                False,
                "Empty username"
            ),
            (
                ['client_user', ''],
                False,
                "Empty password"
            ),
            (
                ['nonexistent', 'Test123!@'],
                False,
                "Non-existent user"
            )
        ]
        
        for inputs, expected_result, desc in test_cases:
            mock_input.side_effect = inputs
            result = self.login_manager.login_interface()
            self.assertEqual(result, expected_result, f"Failed case: {desc}")

    @patch('builtins.print')
    def test_privilege_display(self, mock_print):
        """Test privilege display for all roles"""
        for username, (_, role) in self.test_users.items():
            self.login_manager.display_user_privileges(username, role)
            # Verify print calls
            mock_print.assert_any_call(f"Username: {username}")
            mock_print.assert_any_call(f"Role: {role.value}")

    def test_login_session_handling(self):
        """Test multiple login attempts and session handling"""
        # Test successful login followed by another attempt
        success1, role1 = self.login_manager.login("client_user", "Test123!@")
        self.assertTrue(success1)
        
        # Test immediate second login
        success2, role2 = self.login_manager.login("premium_user", "Test123!@")
        self.assertTrue(success2)
        self.assertNotEqual(role1, role2)

if __name__ == '__main__':
    unittest.main()