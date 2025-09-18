from ninja import Schema
from typing import Optional
from decimal import Decimal
from datetime import datetime, date, time


class CategorySchema(Schema):
    """Schema for Category model - read-only"""
    id: int
    name: str
    category_type: str
    category_type_display: str  # Human readable category type
    icon: str
    color: str
    description: str
    is_active: bool
    parent_id: Optional[int]
    parent_name: Optional[str]  # From related parent Category model
    full_path: str  # Full category path including parents
    created_at: datetime
    updated_at: datetime


class TransactionSchema(Schema):
    """Schema for Transaction model - read-only"""
    id: int
    account_id: int
    account_name: str  # From related Account model
    username: str  # From related User model
    transaction_type: str
    transaction_type_display: str  # Human readable transaction type
    category_id: Optional[int]
    category_name: Optional[str]  # From related Category model
    amount: Decimal
    title: str
    description: str
    date: date
    time: time
    payment_method: str
    payment_method_display: str  # Human readable payment method
    to_account_id: Optional[int]
    to_account_name: Optional[str]  # From related Account model for transfers
    merchant: str
    location: str
    tags: str
    tags_list: list[str]  # Parsed tags as list
    receipt_image: Optional[str]  # URL to receipt image
    is_recurring: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    created_by_id: Optional[int]
    created_by_username: Optional[str]  # From related User model


class RecurringTransactionSchema(Schema):
    """Schema for RecurringTransaction model - read-only"""
    id: int
    user_id: int
    username: str  # From related User model
    account_id: int
    account_name: str  # From related Account model
    transaction_type: str
    transaction_type_display: str  # Human readable transaction type
    category_id: Optional[int]
    category_name: Optional[str]  # From related Category model
    amount: Decimal
    title: str
    description: str
    frequency: str
    frequency_display: str  # Human readable frequency
    start_date: date
    end_date: Optional[date]
    next_due_date: date
    is_active: bool
    auto_create: bool
    created_at: datetime
    updated_at: datetime


class TransactionSummarySchema(Schema):
    """Schema for Transaction summary with aggregated data"""
    id: int
    account_id: int
    account_name: str
    username: str
    transaction_type: str
    transaction_type_display: str
    category_id: Optional[int]
    category_name: Optional[str]
    amount: Decimal
    title: str
    date: date
    payment_method: str
    payment_method_display: str
    merchant: str
    is_recurring: bool
    is_verified: bool
    # Summary fields
    total_income: Decimal
    total_expense: Decimal
    net_amount: Decimal  # total_income - total_expense
    created_at: datetime


class CategoryListResponse(Schema):
    """Response schema for category list with pagination"""
    categories: list[CategorySchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class TransactionListResponse(Schema):
    """Response schema for transaction list with pagination"""
    transactions: list[TransactionSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class RecurringTransactionListResponse(Schema):
    """Response schema for recurring transaction list with pagination"""
    recurring_transactions: list[RecurringTransactionSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int
