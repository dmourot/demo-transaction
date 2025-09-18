from ninja import NinjaAPI, Query
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from typing import Optional
from math import ceil

from .models import Account, UserProfile, Budget
from .schemas import (
    AccountSchema, UserProfileSchema, BudgetSchema,
    AccountListResponse, UserProfileListResponse, BudgetListResponse,
    AccountSummarySchema
)


# Create API instance
api = NinjaAPI(
    title="Accounts API",
    description="Read-only API for accounts, user profiles, and budgets",
    version="1.0.0"
)


def get_username(user):
    """Helper function to get username from user object"""
    return user.username if user else None


def get_category_name(category):
    """Helper function to get category name from category object"""
    return category.name if category else None


@api.get("/accounts/", response=AccountListResponse)
def list_accounts(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    account_type: Optional[str] = Query(None, description="Filter by account type"),
    currency: Optional[str] = Query(None, description="Filter by currency"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in account name and description"),
    user_id: Optional[int] = Query(None, description="Filter by user ID")
):
    """
    List all accounts with optional filtering and pagination.
    """
    queryset = Account.objects.select_related('user').all()
    
    # Apply filters
    if account_type:
        queryset = queryset.filter(account_type=account_type)
    
    if currency:
        queryset = queryset.filter(currency=currency)
    
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    
    if search:
        queryset = queryset.filter(
            Q(account_name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    # Convert to schema
    accounts = []
    for account in page_obj:
        accounts.append(AccountSchema(
            id=account.id,
            user_id=account.user_id,
            username=get_username(account.user),
            account_name=account.account_name,
            account_type=account.account_type,
            account_type_display=account.get_account_type_display(),
            account_number=account.account_number,
            balance=account.balance,
            initial_balance=account.initial_balance,
            currency=account.currency,
            currency_display=account.get_currency_display(),
            description=account.description,
            is_active=account.is_active,
            created_at=account.created_at,
            updated_at=account.updated_at
        ))
    
    return AccountListResponse(
        accounts=accounts,
        total_count=paginator.count,
        page=page,
        page_size=page_size,
        total_pages=ceil(paginator.count / page_size)
    )


@api.get("/accounts/{account_id}/", response=AccountSchema)
def get_account(request, account_id: int):
    """
    Get a specific account by ID.
    """
    account = get_object_or_404(Account.objects.select_related('user'), id=account_id)
    
    return AccountSchema(
        id=account.id,
        user_id=account.user_id,
        username=get_username(account.user),
        account_name=account.account_name,
        account_type=account.account_type,
        account_type_display=account.get_account_type_display(),
        account_number=account.account_number,
        balance=account.balance,
        initial_balance=account.initial_balance,
        currency=account.currency,
        currency_display=account.get_currency_display(),
        description=account.description,
        is_active=account.is_active,
        created_at=account.created_at,
        updated_at=account.updated_at
    )


@api.get("/accounts/{account_id}/summary/", response=AccountSummarySchema)
def get_account_summary(request, account_id: int):
    """
    Get account summary with income/expense totals.
    """
    account = get_object_or_404(Account.objects.select_related('user'), id=account_id)
    
    total_income = account.get_total_income()
    total_expense = account.get_total_expense()
    net_balance = account.balance + total_income - total_expense
    
    return AccountSummarySchema(
        id=account.id,
        user_id=account.user_id,
        username=get_username(account.user),
        account_name=account.account_name,
        account_type=account.account_type,
        account_type_display=account.get_account_type_display(),
        balance=account.balance,
        currency=account.currency,
        currency_display=account.get_currency_display(),
        is_active=account.is_active,
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        created_at=account.created_at
    )


@api.get("/user-profiles/", response=UserProfileListResponse)
def list_user_profiles(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    search: Optional[str] = Query(None, description="Search in username")
):
    """
    List all user profiles with optional filtering and pagination.
    """
    queryset = UserProfile.objects.select_related('user').all()
    
    # Apply filters
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    
    if search:
        queryset = queryset.filter(user__username__icontains=search)
    
    # Pagination
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    # Convert to schema
    profiles = []
    for profile in page_obj:
        profiles.append(UserProfileSchema(
            id=profile.id,
            user_id=profile.user_id,
            username=get_username(profile.user),
            phone_number=profile.phone_number,
            date_of_birth=profile.date_of_birth,
            address=profile.address,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        ))
    
    return UserProfileListResponse(
        profiles=profiles,
        total_count=paginator.count,
        page=page,
        page_size=page_size,
        total_pages=ceil(paginator.count / page_size)
    )


@api.get("/user-profiles/{profile_id}/", response=UserProfileSchema)
def get_user_profile(request, profile_id: int):
    """
    Get a specific user profile by ID.
    """
    profile = get_object_or_404(UserProfile.objects.select_related('user'), id=profile_id)
    
    return UserProfileSchema(
        id=profile.id,
        user_id=profile.user_id,
        username=get_username(profile.user),
        phone_number=profile.phone_number,
        date_of_birth=profile.date_of_birth,
        address=profile.address,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@api.get("/budgets/", response=BudgetListResponse)
def list_budgets(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    period: Optional[str] = Query(None, description="Filter by budget period"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in budget name")
):
    """
    List all budgets with optional filtering and pagination.
    """
    queryset = Budget.objects.select_related('user', 'category').all()
    
    # Apply filters
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    
    if period:
        queryset = queryset.filter(period=period)
    
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    
    if search:
        queryset = queryset.filter(name__icontains=search)
    
    # Pagination
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    # Convert to schema
    budgets = []
    for budget in page_obj:
        spent_amount = budget.get_spent_amount()
        remaining_budget = budget.get_remaining_budget()
        percentage_used = budget.get_percentage_used()
        
        budgets.append(BudgetSchema(
            id=budget.id,
            user_id=budget.user_id,
            username=get_username(budget.user),
            name=budget.name,
            category_id=budget.category_id,
            category_name=get_category_name(budget.category),
            amount=budget.amount,
            period=budget.period,
            period_display=budget.get_period_display(),
            start_date=budget.start_date,
            end_date=budget.end_date,
            is_active=budget.is_active,
            spent_amount=spent_amount,
            remaining_budget=remaining_budget,
            percentage_used=percentage_used,
            created_at=budget.created_at,
            updated_at=budget.updated_at
        ))
    
    return BudgetListResponse(
        budgets=budgets,
        total_count=paginator.count,
        page=page,
        page_size=page_size,
        total_pages=ceil(paginator.count / page_size)
    )


@api.get("/budgets/{budget_id}/", response=BudgetSchema)
def get_budget(request, budget_id: int):
    """
    Get a specific budget by ID.
    """
    budget = get_object_or_404(Budget.objects.select_related('user', 'category'), id=budget_id)
    
    spent_amount = budget.get_spent_amount()
    remaining_budget = budget.get_remaining_budget()
    percentage_used = budget.get_percentage_used()
    
    return BudgetSchema(
        id=budget.id,
        user_id=budget.user_id,
        username=get_username(budget.user),
        name=budget.name,
        category_id=budget.category_id,
        category_name=get_category_name(budget.category),
        amount=budget.amount,
        period=budget.period,
        period_display=budget.get_period_display(),
        start_date=budget.start_date,
        end_date=budget.end_date,
        is_active=budget.is_active,
        spent_amount=spent_amount,
        remaining_budget=remaining_budget,
        percentage_used=percentage_used,
        created_at=budget.created_at,
        updated_at=budget.updated_at
    )


@api.get("/accounts/statistics/")
def get_accounts_statistics(request):
    """
    Get general statistics about accounts.
    """
    total_accounts = Account.objects.count()
    active_accounts = Account.objects.filter(is_active=True).count()
    
    # Account type distribution
    account_types = Account.objects.values('account_type').annotate(
        count=Sum('id', distinct=True)
    ).values('account_type', 'count')
    
    # Currency distribution
    currencies = Account.objects.values('currency').annotate(
        count=Sum('id', distinct=True)
    ).values('currency', 'count')
    
    # Total balance by currency
    balance_by_currency = Account.objects.values('currency').annotate(
        total_balance=Sum('balance')
    ).values('currency', 'total_balance')
    
    return {
        "total_accounts": total_accounts,
        "active_accounts": active_accounts,
        "inactive_accounts": total_accounts - active_accounts,
        "account_types": list(account_types),
        "currencies": list(currencies),
        "balance_by_currency": list(balance_by_currency)
    }
