from enum import Enum, auto
from datetime import datetime, time

class Role(Enum):
    CLIENT = auto()
    PREMIUM_CLIENT = auto()
    FINANCIAL_ADVISOR = auto()
    FINANCIAL_PLANNER = auto()
    TELLER = auto()

class Permission(Enum):
    VIEW_BALANCE = auto()
    VIEW_PORTFOLIO = auto()
    MODIFY_PORTFOLIO = auto()
    VIEW_ADVISOR_CONTACT = auto()
    VIEW_PLANNER_CONTACT = auto()
    VIEW_MONEY_MARKET = auto()
    VIEW_PRIVATE_CONSUMER = auto()
    ACCESS_BUSINESS_HOURS = auto()

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class AccessControl:
    def __init__(self):
        self.role_permissions = {
            Role.CLIENT: {Permission.VIEW_BALANCE, Permission.VIEW_PORTFOLIO, Permission.VIEW_ADVISOR_CONTACT},
            Role.PREMIUM_CLIENT: {Permission.VIEW_BALANCE, Permission.VIEW_PORTFOLIO, Permission.MODIFY_PORTFOLIO, Permission.VIEW_PLANNER_CONTACT},
            Role.FINANCIAL_ADVISOR: {Permission.VIEW_BALANCE, Permission.VIEW_PORTFOLIO, Permission.MODIFY_PORTFOLIO, Permission.VIEW_PRIVATE_CONSUMER},
            Role.FINANCIAL_PLANNER: {Permission.VIEW_BALANCE, Permission.VIEW_PORTFOLIO, Permission.MODIFY_PORTFOLIO, Permission.VIEW_MONEY_MARKET, Permission.VIEW_PRIVATE_CONSUMER},
            Role.TELLER: {Permission.VIEW_BALANCE, Permission.VIEW_PORTFOLIO, Permission.ACCESS_BUSINESS_HOURS}
        }

    def check_permission(self, user, permission):
        if user.role == Role.TELLER:
            if not self._check_business_hours():
                return False
        return permission in self.role_permissions[user.role]

    def _check_business_hours(self):
        now = datetime.now().time()
        return time(9, 0) <= now <= time(17, 0)

    def get_user_permissions(self, role):
        return self.role_permissions[role]

# Test cases
def run_tests():
    ac = AccessControl()
    
    client = User("john_doe", Role.CLIENT)
    assert ac.check_permission(client, Permission.VIEW_BALANCE) == True
    assert ac.check_permission(client, Permission.MODIFY_PORTFOLIO) == False

    premium_client = User("jane_smith", Role.PREMIUM_CLIENT)
    assert ac.check_permission(premium_client, Permission.MODIFY_PORTFOLIO) == True
    assert ac.check_permission(premium_client, Permission.VIEW_MONEY_MARKET) == False

    advisor = User("mike_johnson", Role.FINANCIAL_ADVISOR)
    assert ac.check_permission(advisor, Permission.VIEW_PRIVATE_CONSUMER) == True
    assert ac.check_permission(advisor, Permission.VIEW_MONEY_MARKET) == False

    planner = User("sarah_lee", Role.FINANCIAL_PLANNER)
    assert ac.check_permission(planner, Permission.VIEW_MONEY_MARKET) == True
    assert ac.check_permission(planner, Permission.VIEW_PRIVATE_CONSUMER) == True

    teller = User("tom_brown", Role.TELLER)
    assert ac.check_permission(teller, Permission.VIEW_BALANCE) == True
    assert ac.check_permission(teller, Permission.MODIFY_PORTFOLIO) == False

    teller = User("tom_brown", Role.TELLER)
    ac._check_business_hours = lambda: True
    assert ac.check_permission(teller, Permission.VIEW_BALANCE) == True
    ac._check_business_hours = lambda: False
    assert ac.check_permission(teller, Permission.VIEW_BALANCE) == False

    print("All test cases passed successfully!")

if __name__ == "__main__":
    run_tests()