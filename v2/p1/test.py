import unittest
from datetime import datetime
import mock
from main import AccessControl, Role, Operation, User

class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.ac = AccessControl()
        self.test_users = {
            "sasha.kim": User("sasha.kim", Role.CLIENT),
            "noor.abbasi": User("noor.abbasi", Role.PREMIUM_CLIENT),
            "mikael.chen": User("mikael.chen", Role.FINANCIAL_ADVISOR),
            "ellis.nakamura": User("ellis.nakamura", Role.FINANCIAL_PLANNER),
            "alex.hayes": User("alex.hayes", Role.TELLER)
        }

    def test_role_initialization(self):
        """Test that all roles are properly initialized with permissions"""
        for role in Role:
            permissions = self.ac.get_user_permissions(role)
            self.assertIsInstance(permissions, set)
            self.assertTrue(len(permissions) > 0)

    def test_client_permissions(self):
        """Test Client role permissions"""
        user = self.test_users["sasha.kim"]
        
        # Test allowed operations
        allowed_ops = {
            Operation.VIEW_BALANCE,
            Operation.VIEW_PORTFOLIO,
            Operation.VIEW_FA_CONTACT
        }
        for op in allowed_ops:
            self.assertTrue(self.ac.check_permission(user.role, op))

        # Test denied operations
        denied_ops = {
            Operation.MODIFY_PORTFOLIO,
            Operation.VIEW_FP_CONTACT,
            Operation.VIEW_MARKET_INSTRUMENTS,
            Operation.VIEW_PRIVATE_INSTRUMENTS
        }
        for op in denied_ops:
            self.assertFalse(self.ac.check_permission(user.role, op))

    def test_premium_client_permissions(self):
        """Test Premium Client role permissions"""
        user = self.test_users["noor.abbasi"]
        
        # Test allowed operations
        allowed_ops = {
            Operation.VIEW_BALANCE,
            Operation.VIEW_PORTFOLIO,
            Operation.MODIFY_PORTFOLIO,
            Operation.VIEW_FP_CONTACT
        }
        for op in allowed_ops:
            self.assertTrue(self.ac.check_permission(user.role, op))

        # Test denied operations
        denied_ops = {
            Operation.VIEW_FA_CONTACT,
            Operation.VIEW_MARKET_INSTRUMENTS,
            Operation.VIEW_PRIVATE_INSTRUMENTS
        }
        for op in denied_ops:
            self.assertFalse(self.ac.check_permission(user.role, op))

    def test_financial_advisor_permissions(self):
        """Test Financial Advisor role permissions"""
        user = self.test_users["mikael.chen"]
        
        # Test allowed operations
        allowed_ops = {
            Operation.VIEW_BALANCE,
            Operation.VIEW_PORTFOLIO,
            Operation.MODIFY_PORTFOLIO,
            Operation.VIEW_PRIVATE_INSTRUMENTS
        }
        for op in allowed_ops:
            self.assertTrue(self.ac.check_permission(user.role, op))

        # Test denied operations
        denied_ops = {
            Operation.VIEW_FA_CONTACT,
            Operation.VIEW_FP_CONTACT,
            Operation.VIEW_MARKET_INSTRUMENTS
        }
        for op in denied_ops:
            self.assertFalse(self.ac.check_permission(user.role, op))

    def test_financial_planner_permissions(self):
        """Test Financial Planner role permissions"""
        user = self.test_users["ellis.nakamura"]
        
        # Test allowed operations
        allowed_ops = {
            Operation.VIEW_BALANCE,
            Operation.VIEW_PORTFOLIO,
            Operation.MODIFY_PORTFOLIO,
            Operation.VIEW_MARKET_INSTRUMENTS,
            Operation.VIEW_PRIVATE_INSTRUMENTS
        }
        for op in allowed_ops:
            self.assertTrue(self.ac.check_permission(user.role, op))

        # Test denied operations
        denied_ops = {
            Operation.VIEW_FA_CONTACT,
            Operation.VIEW_FP_CONTACT
        }
        for op in denied_ops:
            self.assertFalse(self.ac.check_permission(user.role, op))

    @mock.patch('main.datetime')
    def test_teller_time_restrictions(self, mock_datetime):
        """Test Teller role time-based access restrictions"""
        user = self.test_users["alex.hayes"]
        operations = [Operation.VIEW_BALANCE, Operation.VIEW_PORTFOLIO]
        
        # Test various times
        test_hours = {
            8: False,   # Before hours
            9: True,    # Start of hours
            14: True,   # During hours
            16: True,   # End of hours
            17: False,  # After hours
            20: False   # Evening
        }
        
        for hour, should_allow in test_hours.items():
            mock_datetime.now.return_value.hour = hour
            for op in operations:
                self.assertEqual(
                    self.ac.check_permission(user.role, op),
                    should_allow,
                    f"Failed at hour {hour} for operation {op}"
                )

    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        # Test invalid role
        self.assertEqual(self.ac.get_user_permissions(None), set())
        
        # Test invalid operation
        self.assertFalse(self.ac.check_permission(Role.CLIENT, None))
        self.assertFalse(self.ac.check_permission(Role.CLIENT, "invalid"))
        
        # Test invalid role and operation
        self.assertFalse(self.ac.check_permission(None, None))

    def test_permission_isolation(self):
        """Test that roles cannot access other roles' permissions"""
        for username, user in self.test_users.items():
            permissions = self.ac.get_user_permissions(user.role)
            other_roles = [r for r in Role if r != user.role]
            
            for other_role in other_roles:
                other_permissions = self.ac.get_user_permissions(other_role)
                self.assertNotEqual(permissions, other_permissions)

if __name__ == '__main__':
    unittest.main()