import unittest
from problem1 import AccessControl, Role, Permission, User
from problem2 import PasswordManager
from problem3 import EnrollmentSystem
from problem4 import app

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.access_control = AccessControl()
        self.password_manager = PasswordManager('test_passwd.txt')
        self.enrollment_system = EnrollmentSystem()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.app = app.test_client()

    def test_enrollment_and_login(self):
        # Test user enrollment
        success, result = self.enrollment_system.enroll_user(
            "test@example.com",
            "ValidP@ss1!",
            "CLIENT"
        )
        self.assertTrue(success)

        # Test login with enrolled user
        response = self.app.post('/login', json={
            'username': 'test@example.com',
            'password': 'ValidP@ss1!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.get_json()['message'])

    def test_access_control(self):
        # Enroll users with different roles
        roles = ['CLIENT', 'PREMIUM_CLIENT', 'FINANCIAL_ADVISOR', 'FINANCIAL_PLANNER', 'TELLER']
        for i, role in enumerate(roles):
            self.enrollment_system.enroll_user(
                f"user{i}@example.com",
                f"ValidP@ss{i}!",
                role
            )

        # Test permissions for each role
        for i, role in enumerate(roles):
            user = User(f"user{i}@example.com", Role[role])
            permissions = self.access_control.get_user_permissions(Role[role])
            
            if role == 'CLIENT':
                self.assertIn(Permission.VIEW_BALANCE, permissions)
                self.assertNotIn(Permission.MODIFY_PORTFOLIO, permissions)
            elif role == 'PREMIUM_CLIENT':
                self.assertIn(Permission.MODIFY_PORTFOLIO, permissions)
                self.assertIn(Permission.VIEW_PLANNER_CONTACT, permissions)
            elif role == 'FINANCIAL_ADVISOR':
                self.assertIn(Permission.VIEW_PRIVATE_CONSUMER, permissions)
                self.assertNotIn(Permission.VIEW_MONEY_MARKET, permissions)
            elif role == 'FINANCIAL_PLANNER':
                self.assertIn(Permission.VIEW_MONEY_MARKET, permissions)
                self.assertIn(Permission.VIEW_PRIVATE_CONSUMER, permissions)
            elif role == 'TELLER':
                self.assertIn(Permission.ACCESS_BUSINESS_HOURS, permissions)
                self.assertNotIn(Permission.MODIFY_PORTFOLIO, permissions)

    def test_teller_business_hours(self):
        teller = User("teller@example.com", Role.TELLER)
        
        # Simulate business hours
        self.access_control._check_business_hours = lambda: True
        self.assertTrue(self.access_control.check_permission(teller, Permission.VIEW_BALANCE))
        
        # Simulate outside business hours
        self.access_control._check_business_hours = lambda: False
        self.assertFalse(self.access_control.check_permission(teller, Permission.VIEW_BALANCE))

    def test_user_info(self):
        with self.app as client:
            # Enroll and login a user
            self.enrollment_system.enroll_user("advisor@example.com", "ValidP@ss1!", "FINANCIAL_ADVISOR")
            client.post('/login', json={
                'username': 'advisor@example.com',
                'password': 'ValidP@ss1!'
            })

            # Test user info retrieval
            response = client.get('/user_info')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['username'], 'advisor@example.com')
            self.assertEqual(data['role'], 'FINANCIAL_ADVISOR')
            self.assertIn('VIEW_PORTFOLIO', data['permissions'])
            self.assertIn('MODIFY_PORTFOLIO', data['permissions'])
            self.assertIn('VIEW_PRIVATE_CONSUMER', data['permissions'])

    def tearDown(self):
        import os
        if os.path.exists('test_passwd.txt'):
            os.remove('test_passwd.txt')

if __name__ == '__main__':
    unittest.main()