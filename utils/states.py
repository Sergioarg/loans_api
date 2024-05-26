""" Unums with general states of models """
from enum import Enum

class PaymentStatus(Enum):
    COMPLETED = 1
    REJECTED = 2

class CustomerStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2

class LoanStatus(Enum):
    INITIAL = 0
    PENDING = 1
    ACTIVE = 2
    REJECTED = 3
    PAID = 4

