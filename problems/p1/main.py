from enum import Enum
from datetime import datetime
from typing import List, Set

class Role(Enum):
    CLIENT = "Client"
    PREMIUM_CLIENT = "Premium Client"
    FINANCIAL_ADVISOR = "Financial Advisor"
    FINANCIAL_PLANNER = "Financial Planner"
    TELLER = "Teller"

class Operation(Enum):
    VIEW_BALANCE = "View account balance"
    VIEW_PORTFOLIO = "View investment portfolio"
    MODIFY_PORTFOLIO = "Modify investment portfolio"
    VIEW_FA_CONTACT = "View Financial Advisor contact"
    VIEW_FP_CONTACT = "View Financial Planner contact"
    VIEW_MARKET_INSTRUMENTS = "View money market instruments"
    VIEW_PRIVATE_INSTRUMENTS = "View private consumer instruments"
class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role
class AccessControl:
    def __init__(self):
        self._init_permissions()

    def _init_permissions(self):
        """Initialize role-based permissions"""
        self.role_permissions = {
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

    def get_user_permissions(self, role: Role) -> Set[Operation]:
        """Get permissions for a given role"""
        if not isinstance(role, Role):
            return set()
        return self.role_permissions.get(role, set())

    def check_permission(self, role: Role, operation: Operation) -> bool:
        """Check if a role has a specific permission"""
        if not isinstance(operation, Operation):
            return False
            
        if role == Role.TELLER:
            current_hour = datetime.now().hour
            if not (9 <= current_hour < 17):
                return False
                
        return operation in self.role_permissions.get(role, set())