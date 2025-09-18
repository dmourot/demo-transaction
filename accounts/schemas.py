from ninja import Schema
from typing import Optional
from decimal import Decimal
from datetime import datetime, date


class UserProfileSchema(Schema):
    """Schema for UserProfile model - read-only"""
    id: int
    user_id: int
    username: str  # From related User model
    phone_number: str
    date_of_birth: Optional[date]
    address: str
    created_at: datetime
    updated_at: datetime


class AccountSchema(Schema):
    """Schema for Account model - read-only"""
    id: int
    user_id: int
    username: str  # From related User model
    account_name: str
    account_type: str
    account_type_display: str  # Human readable account type
    account_number: str
    balance: Decimal
    initial_balance: Decimal
    currency: str
    currency_display: str  # Human readable currency
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AccountSummarySchema(Schema):
    """Schema for Account with summary data"""
    id: int
    user_id: int
    username: str
    account_name: str
    account_type: str
    account_type_display: str
    balance: Decimal
    currency: str
    currency_display: str
    is_active: bool
    total_income: Decimal
    total_expense: Decimal
    net_balance: Decimal  # balance + total_income - total_expense
    created_at: datetime


class BudgetSchema(Schema):
    """Schema for Budget model - read-only"""
    id: int
    user_id: int
    username: str  # From related User model
    name: str
    category_id: Optional[int]
    category_name: Optional[str]  # From related Category model
    amount: Decimal
    period: str
    period_display: str  # Human readable period
    start_date: date
    end_date: Optional[date]
    is_active: bool
    spent_amount: Decimal
    remaining_budget: Decimal
    percentage_used: float
    created_at: datetime
    updated_at: datetime


class AccountListResponse(Schema):
    """Response schema for account list with pagination"""
    accounts: list[AccountSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class UserProfileListResponse(Schema):
    """Response schema for user profile list with pagination"""
    profiles: list[UserProfileSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class BudgetListResponse(Schema):
    """Response schema for budget list with pagination"""
    budgets: list[BudgetSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int
