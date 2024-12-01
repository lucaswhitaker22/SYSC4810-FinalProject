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

    def test_client_permissions(self):
        user = self.test_users["sasha.kim"]
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_BALANCE))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_PORTFOLIO))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_FA_CONTACT))
        self.assertFalse(self.ac.check_permission(user.role, Operation.MODIFY_PORTFOLIO))
        self.assertFalse(self.ac.check_permission(user.role, Operation.VIEW_FP_CONTACT))

    def test_premium_client_permissions(self):
        user = self.test_users["noor.abbasi"]
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_BALANCE))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_PORTFOLIO))
        self.assertTrue(self.ac.check_permission(user.role, Operation.MODIFY_PORTFOLIO))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_FP_CONTACT))
        self.assertFalse(self.ac.check_permission(user.role, Operation.VIEW_MARKET_INSTRUMENTS))

    def test_financial_advisor_permissions(self):
        user = self.test_users["mikael.chen"]
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_BALANCE))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_PORTFOLIO))
        self.assertTrue(self.ac.check_permission(user.role, Operation.MODIFY_PORTFOLIO))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_PRIVATE_INSTRUMENTS))
        self.assertFalse(self.ac.check_permission(user.role, Operation.VIEW_MARKET_INSTRUMENTS))

    def test_financial_planner_permissions(self):
        user = self.test_users["ellis.nakamura"]
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_BALANCE))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_PORTFOLIO))
        self.assertTrue(self.ac.check_permission(user.role, Operation.MODIFY_PORTFOLIO))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_MARKET_INSTRUMENTS))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_PRIVATE_INSTRUMENTS))


    @mock.patch('main.datetime')
    def test_teller_permissions_during_hours(self, mock_datetime):
        user = self.test_users["alex.hayes"]
        # Mock 2 PM
        mock_datetime.now.return_value.hour = 14
        
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_BALANCE))
        self.assertTrue(self.ac.check_permission(user.role, Operation.VIEW_PORTFOLIO))
        self.assertFalse(self.ac.check_permission(user.role, Operation.MODIFY_PORTFOLIO))

    @mock.patch('main.datetime')
    def test_teller_permissions_after_hours(self, mock_datetime):
        user = self.test_users["alex.hayes"]
        # Mock 8 PM
        mock_datetime.now.return_value.hour = 20
        
        self.assertFalse(self.ac.check_permission(user.role, Operation.VIEW_BALANCE))
        self.assertFalse(self.ac.check_permission(user.role, Operation.VIEW_PORTFOLIO))

    def test_get_user_permissions(self):
        for username, user in self.test_users.items():
            permissions = self.ac.get_user_permissions(user.role)
            self.assertIsInstance(permissions, set)
            self.assertTrue(len(permissions) > 0)

    def test_unauthorized_operations(self):
        for username, user in self.test_users.items():
            self.assertFalse(self.ac.check_permission(user.role, None))
            self.assertFalse(self.ac.check_permission(user.role, "INVALID_OPERATION"))

if __name__ == '__main__':
    unittest.main()