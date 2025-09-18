from ninja import NinjaAPI, Query
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from typing import Optional
from math import ceil
from decimal import Decimal

from .models import Transaction, Category, RecurringTransaction
from .schemas import (
    TransactionSchema, CategorySchema, RecurringTransactionSchema,
    TransactionListResponse, CategoryListResponse, RecurringTransactionListResponse,
    TransactionSummarySchema
)


# Create API instance
api = NinjaAPI(
    title="Transactions API",
    description="Read-only API for transactions, categories, and recurring transactions",
    version="1.0.0"
)


def get_username(user):
    """Helper function to get username from user object"""
    return user.username if user else None


def get_account_name(account):
    """Helper function to get account name from account object"""
    return account.account_name if account else None


def get_category_name(category):
    """Helper function to get category name from category object"""
    return category.name if category else None


def get_parent_category_name(category):
    """Helper function to get parent category name from category object"""
    return category.parent.name if category and category.parent else None


@api.get("/categories/", response=CategoryListResponse)
def list_categories(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    category_type: Optional[str] = Query(None, description="Filter by category type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
    search: Optional[str] = Query(None, description="Search in category name and description")
):
    """
    List all categories with optional filtering and pagination.
    """
    queryset = Category.objects.select_related('parent').all()
    
    # Apply filters
    if category_type:
        queryset = queryset.filter(category_type=category_type)
    
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    
    if parent_id is not None:
        if parent_id == 0:
            # Show only root categories (no parent)
            queryset = queryset.filter(parent__isnull=True)
        else:
            queryset = queryset.filter(parent_id=parent_id)
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    # Convert to schema
    categories = []
    for category in page_obj:
        categories.append(CategorySchema(
            id=category.id,
            name=category.name,
            category_type=category.category_type,
            category_type_display=category.get_category_type_display(),
            icon=category.icon,
            color=category.color,
            description=category.description,
            is_active=category.is_active,
            parent_id=category.parent_id,
            parent_name=get_parent_category_name(category),
            full_path=category.get_full_path(),
            created_at=category.created_at,
            updated_at=category.updated_at
        ))
    
    return CategoryListResponse(
        categories=categories,
        total_count=paginator.count,
        page=page,
        page_size=page_size,
        total_pages=ceil(paginator.count / page_size)
    )


@api.get("/categories/{category_id}/", response=CategorySchema)
def get_category(request, category_id: int):
    """
    Get a specific category by ID.
    """
    category = get_object_or_404(Category.objects.select_related('parent'), id=category_id)
    
    return CategorySchema(
        id=category.id,
        name=category.name,
        category_type=category.category_type,
        category_type_display=category.get_category_type_display(),
        icon=category.icon,
        color=category.color,
        description=category.description,
        is_active=category.is_active,
        parent_id=category.parent_id,
        parent_name=get_parent_category_name(category),
        full_path=category.get_full_path(),
        created_at=category.created_at,
        updated_at=category.updated_at
    )


@api.get("/transactions/", response=TransactionListResponse)
def list_transactions(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    transaction_type: Optional[str] = Query(None, description="Filter by transaction type"),
    account_id: Optional[int] = Query(None, description="Filter by account ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    payment_method: Optional[str] = Query(None, description="Filter by payment method"),
    is_recurring: Optional[bool] = Query(None, description="Filter by recurring status"),
    is_verified: Optional[bool] = Query(None, description="Filter by verified status"),
    date_from: Optional[str] = Query(None, description="Filter transactions from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter transactions to date (YYYY-MM-DD)"),
    min_amount: Optional[float] = Query(None, description="Filter by minimum amount"),
    max_amount: Optional[float] = Query(None, description="Filter by maximum amount"),
    search: Optional[str] = Query(None, description="Search in title, description, and merchant"),
    user_id: Optional[int] = Query(None, description="Filter by user ID")
):
    """
    List all transactions with optional filtering and pagination.
    """
    queryset = Transaction.objects.select_related(
        'account', 'account__user', 'category', 'to_account', 'created_by'
    ).all()
    
    # Apply filters
    if transaction_type:
        queryset = queryset.filter(transaction_type=transaction_type)
    
    if account_id:
        queryset = queryset.filter(account_id=account_id)
    
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    
    if payment_method:
        queryset = queryset.filter(payment_method=payment_method)
    
    if is_recurring is not None:
        queryset = queryset.filter(is_recurring=is_recurring)
    
    if is_verified is not None:
        queryset = queryset.filter(is_verified=is_verified)
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    
    if min_amount is not None:
        queryset = queryset.filter(amount__gte=min_amount)
    
    if max_amount is not None:
        queryset = queryset.filter(amount__lte=max_amount)
    
    if user_id:
        queryset = queryset.filter(account__user_id=user_id)
    
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(merchant__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    # Convert to schema
    transactions = []
    for transaction in page_obj:
        transactions.append(TransactionSchema(
            id=transaction.id,
            account_id=transaction.account_id,
            account_name=get_account_name(transaction.account),
            username=get_username(transaction.account.user),
            transaction_type=transaction.transaction_type,
            transaction_type_display=transaction.get_transaction_type_display(),
            category_id=transaction.category_id,
            category_name=get_category_name(transaction.category),
            amount=transaction.amount,
            title=transaction.title,
            description=transaction.description,
            date=transaction.date,
            time=transaction.time,
            payment_method=transaction.payment_method,
            payment_method_display=transaction.get_payment_method_display(),
            to_account_id=transaction.to_account_id,
            to_account_name=get_account_name(transaction.to_account),
            merchant=transaction.merchant,
            location=transaction.location,
            tags=transaction.tags,
            tags_list=transaction.get_tags_list(),
            receipt_image=str(transaction.receipt_image) if transaction.receipt_image else None,
            is_recurring=transaction.is_recurring,
            is_verified=transaction.is_verified,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
            created_by_id=transaction.created_by_id,
            created_by_username=get_username(transaction.created_by)
        ))
    
    return TransactionListResponse(
        transactions=transactions,
        total_count=paginator.count,
        page=page,
        page_size=page_size,
        total_pages=ceil(paginator.count / page_size)
    )


@api.get("/transactions/{transaction_id}/", response=TransactionSchema)
def get_transaction(request, transaction_id: int):
    """
    Get a specific transaction by ID.
    """
    transaction = get_object_or_404(
        Transaction.objects.select_related(
            'account', 'account__user', 'category', 'to_account', 'created_by'
        ), 
        id=transaction_id
    )
    
    return TransactionSchema(
        id=transaction.id,
        account_id=transaction.account_id,
        account_name=get_account_name(transaction.account),
        username=get_username(transaction.account.user),
        transaction_type=transaction.transaction_type,
        transaction_type_display=transaction.get_transaction_type_display(),
        category_id=transaction.category_id,
        category_name=get_category_name(transaction.category),
        amount=transaction.amount,
        title=transaction.title,
        description=transaction.description,
        date=transaction.date,
        time=transaction.time,
        payment_method=transaction.payment_method,
        payment_method_display=transaction.get_payment_method_display(),
        to_account_id=transaction.to_account_id,
        to_account_name=get_account_name(transaction.to_account),
        merchant=transaction.merchant,
        location=transaction.location,
        tags=transaction.tags,
        tags_list=transaction.get_tags_list(),
        receipt_image=str(transaction.receipt_image) if transaction.receipt_image else None,
        is_recurring=transaction.is_recurring,
        is_verified=transaction.is_verified,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
        created_by_id=transaction.created_by_id,
        created_by_username=get_username(transaction.created_by)
    )


@api.get("/transactions/{transaction_id}/summary/", response=TransactionSummarySchema)
def get_transaction_summary(request, transaction_id: int):
    """
    Get transaction summary with aggregated data.
    """
    transaction = get_object_or_404(
        Transaction.objects.select_related(
            'account', 'account__user', 'category'
        ), 
        id=transaction_id
    )
    
    # Calculate summary data for the account
    account_transactions = Transaction.objects.filter(account=transaction.account)
    total_income = account_transactions.filter(transaction_type='INCOME').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    total_expense = account_transactions.filter(transaction_type='EXPENSE').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    
    net_amount = total_income - total_expense
    
    return TransactionSummarySchema(
        id=transaction.id,
        account_id=transaction.account_id,
        account_name=get_account_name(transaction.account),
        username=get_username(transaction.account.user),
        transaction_type=transaction.transaction_type,
        transaction_type_display=transaction.get_transaction_type_display(),
        category_id=transaction.category_id,
        category_name=get_category_name(transaction.category),
        amount=transaction.amount,
        title=transaction.title,
        date=transaction.date,
        payment_method=transaction.payment_method,
        payment_method_display=transaction.get_payment_method_display(),
        merchant=transaction.merchant,
        is_recurring=transaction.is_recurring,
        is_verified=transaction.is_verified,
        total_income=total_income,
        total_expense=total_expense,
        net_amount=net_amount,
        created_at=transaction.created_at
    )


@api.get("/recurring-transactions/", response=RecurringTransactionListResponse)
def list_recurring_transactions(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    account_id: Optional[int] = Query(None, description="Filter by account ID"),
    transaction_type: Optional[str] = Query(None, description="Filter by transaction type"),
    frequency: Optional[str] = Query(None, description="Filter by frequency"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in title and description")
):
    """
    List all recurring transactions with optional filtering and pagination.
    """
    queryset = RecurringTransaction.objects.select_related(
        'user', 'account', 'category'
    ).all()
    
    # Apply filters
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    
    if account_id:
        queryset = queryset.filter(account_id=account_id)
    
    if transaction_type:
        queryset = queryset.filter(transaction_type=transaction_type)
    
    if frequency:
        queryset = queryset.filter(frequency=frequency)
    
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    # Convert to schema
    recurring_transactions = []
    for recurring in page_obj:
        recurring_transactions.append(RecurringTransactionSchema(
            id=recurring.id,
            user_id=recurring.user_id,
            username=get_username(recurring.user),
            account_id=recurring.account_id,
            account_name=get_account_name(recurring.account),
            transaction_type=recurring.transaction_type,
            transaction_type_display=recurring.get_transaction_type_display(),
            category_id=recurring.category_id,
            category_name=get_category_name(recurring.category),
            amount=recurring.amount,
            title=recurring.title,
            description=recurring.description,
            frequency=recurring.frequency,
            frequency_display=recurring.get_frequency_display(),
            start_date=recurring.start_date,
            end_date=recurring.end_date,
            next_due_date=recurring.next_due_date,
            is_active=recurring.is_active,
            auto_create=recurring.auto_create,
            created_at=recurring.created_at,
            updated_at=recurring.updated_at
        ))
    
    return RecurringTransactionListResponse(
        recurring_transactions=recurring_transactions,
        total_count=paginator.count,
        page=page,
        page_size=page_size,
        total_pages=ceil(paginator.count / page_size)
    )


@api.get("/recurring-transactions/{recurring_id}/", response=RecurringTransactionSchema)
def get_recurring_transaction(request, recurring_id: int):
    """
    Get a specific recurring transaction by ID.
    """
    recurring = get_object_or_404(
        RecurringTransaction.objects.select_related('user', 'account', 'category'), 
        id=recurring_id
    )
    
    return RecurringTransactionSchema(
        id=recurring.id,
        user_id=recurring.user_id,
        username=get_username(recurring.user),
        account_id=recurring.account_id,
        account_name=get_account_name(recurring.account),
        transaction_type=recurring.transaction_type,
        transaction_type_display=recurring.get_transaction_type_display(),
        category_id=recurring.category_id,
        category_name=get_category_name(recurring.category),
        amount=recurring.amount,
        title=recurring.title,
        description=recurring.description,
        frequency=recurring.frequency,
        frequency_display=recurring.get_frequency_display(),
        start_date=recurring.start_date,
        end_date=recurring.end_date,
        next_due_date=recurring.next_due_date,
        is_active=recurring.is_active,
        auto_create=recurring.auto_create,
        created_at=recurring.created_at,
        updated_at=recurring.updated_at
    )


@api.get("/transactions/statistics/")
def get_transactions_statistics(request):
    """
    Get general statistics about transactions.
    """
    total_transactions = Transaction.objects.count()
    verified_transactions = Transaction.objects.filter(is_verified=True).count()
    recurring_transactions = Transaction.objects.filter(is_recurring=True).count()
    
    # Transaction type distribution
    transaction_types = Transaction.objects.values('transaction_type').annotate(
        count=Count('id')
    ).values('transaction_type', 'count')
    
    # Payment method distribution
    payment_methods = Transaction.objects.values('payment_method').annotate(
        count=Count('id')
    ).values('payment_method', 'count')
    
    # Total amounts by transaction type
    amounts_by_type = Transaction.objects.values('transaction_type').annotate(
        total_amount=Sum('amount')
    ).values('transaction_type', 'total_amount')
    
    # Category distribution
    categories = Transaction.objects.values('category__name').annotate(
        count=Count('id')
    ).filter(category__isnull=False).values('category__name', 'count')
    
    # Monthly transaction count (last 12 months)
    from django.db.models.functions import TruncMonth
    monthly_counts = Transaction.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')[:12]
    
    return {
        "total_transactions": total_transactions,
        "verified_transactions": verified_transactions,
        "unverified_transactions": total_transactions - verified_transactions,
        "recurring_transactions": recurring_transactions,
        "transaction_types": list(transaction_types),
        "payment_methods": list(payment_methods),
        "amounts_by_type": list(amounts_by_type),
        "categories": list(categories),
        "monthly_counts": list(monthly_counts)
    }
