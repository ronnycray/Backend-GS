from sqlalchemy import (
    Column, Integer, ForeignKey, Float, VARCHAR, Enum, TIMESTAMP
)
from sqlalchemy.orm import relationship
from services.database import BaseModel
from datetime import datetime
from services.finance.enums import ColorActions, TransactionType


class FinancialBusiness(BaseModel):
    __tablename__ = 'financial_business'
    __tableargs__ = {
        'comment': "Table of manage finances business"
    }

    business_id = Column(
        Integer,
        ForeignKey('business.id', ondelete='CASCADE')
    )
    total_amount = Column(Float, nullable=False, default=0)

    accrual_categories = relationship(
        "AccrualCategories",
        lazy='selectin',
        foreign_keys='[AccrualCategories.financial_business_id]',
        uselist=True
    )
    expense_categories = relationship(
        "ExpenseCategories",
        lazy='selectin',
        foreign_keys='[ExpenseCategories.financial_business_id]',
        uselist=True
    )
    tags = relationship(
        "FinancialTag",
        lazy='selectin',
        foreign_keys='[FinancialTag.financial_business_id]',
        uselist=True
    )
    transactions = relationship(
        "FinancialTransaction",
        lazy='selectin',
        foreign_keys='[FinancialTransaction.financial_business_id]',
        uselist=True
    )
    # business = relationship(
    #     "Business",
    #     lazy='selectin',
    #     foreign_keys=[business_id],
    #     back_populates="financial_account"
    # )

    def __repr__(self):
        return f"FinancialBusiness of {self.business_id} | ID: {self.id}"


class AccrualCategories(BaseModel):
    __tablename__ = 'accrual_categories'
    __tableargs__ = {
        'comment': "Table of accrual categories of business"
    }

    financial_business_id = Column(
        Integer,
        ForeignKey('financial_business.id', ondelete='CASCADE')
    )
    title = Column(VARCHAR(255), nullable=False, default="")
    color = Column(
        Enum(ColorActions, native_enum=False),
        nullable=False,
        default=ColorActions.GREEN
    )
    image = Column(VARCHAR(255), nullable=False, default="")

    financial_business = relationship(
        "FinancialBusiness",
        lazy='selectin',
        foreign_keys=[financial_business_id],
        back_populates="accrual_categories"
    )
    financial_transaction = relationship(
        "FinancialTransaction",
        lazy='selectin',
        foreign_keys='[FinancialTransaction.accrual_category_id]',
        back_populates="accrual"
    )

    def __repr__(self):
        return f"AccrualCategories of {self.financial_business_id} | ID: {self.id}"


class ExpenseCategories(BaseModel):
    __tablename__ = 'expense_categories'
    __tableargs__ = {
        'comment': "Table of expense categories of business"
    }

    financial_business_id = Column(
        Integer,
        ForeignKey('financial_business.id', ondelete='CASCADE')
    )
    title = Column(VARCHAR(255), nullable=False, default="")
    color = Column(
        Enum(ColorActions, native_enum=False),
        nullable=False,
        default=ColorActions.RED
    )
    image = Column(VARCHAR(255), nullable=False, default="")

    financial_business = relationship(
        "FinancialBusiness",
        lazy='selectin',
        foreign_keys=[financial_business_id],
        back_populates="expense_categories"
    )
    financial_transaction = relationship(
        "FinancialTransaction",
        lazy='selectin',
        foreign_keys='[FinancialTransaction.expense_category_id]',
        back_populates="expense"
    )

    def __repr__(self):
        return f"ExpenseCategories of {self.financial_business_id} | ID: {self.id}"


class FinancialTag(BaseModel):
    __tablename__ = 'financial_tag'
    __tableargs__ = {
        'comment': "Table of tags for finance transactions"
    }

    financial_business_id = Column(
        Integer,
        ForeignKey('financial_business.id', ondelete='CASCADE')
    )
    name = Column(VARCHAR(255), nullable=False, default="")

    financial_business = relationship(
        "FinancialBusiness",
        lazy='selectin',
        foreign_keys=[financial_business_id],
        back_populates="tags"
    )

    def __repr__(self):
        return f"FinancialTag of {self.financial_business_id} | ID: {self.id}"


class FinancialTransaction(BaseModel):
    __tablename__ = 'financial_transaction'
    __tableargs__ = {
        'comment': "Table of finance transactions"
    }

    financial_business_id = Column(
        Integer,
        ForeignKey('financial_business.id', ondelete='CASCADE')
    )
    hash_id = Column(VARCHAR(1024), nullable=False, default="", unique=True)
    transaction_type = Column(
        Enum(TransactionType, native_enum=False),
        nullable=False,
        default=TransactionType.ACCRUAL
    )
    expense_category_id = Column(
        Integer,
        ForeignKey('expense_categories.id', ondelete='CASCADE')
    )
    accrual_category_id = Column(
        Integer,
        ForeignKey('accrual_categories.id', ondelete='CASCADE')
    )
    amount = Column(Float, nullable=False, default=0)
    date = Column(TIMESTAMP, nullable=False, default=datetime.now)
    comment = Column(VARCHAR(255), nullable=False, default="")

    financial_business = relationship(
        "FinancialBusiness",
        lazy='selectin',
        foreign_keys=[financial_business_id],
        back_populates="transactions"
    )
    transactions_tags = relationship(
        "TransactionTag",
        lazy='selectin',
        foreign_keys='[TransactionTag.transaction_hash_id]',
        uselist=True
    )
    expense = relationship(
        "ExpenseCategories",
        lazy='selectin',
        foreign_keys=[expense_category_id],
        uselist=False
    )
    accrual = relationship(
        "AccrualCategories",
        lazy='selectin',
        foreign_keys=[accrual_category_id],
        uselist=False
    )

    def __repr__(self):
        return f"FinancialTransaction of {self.financial_business_id} | ID: {self.id}"


class TransactionTag(BaseModel):
    __tablename__ = 'transaction_tag'
    __tableargs__ = {
        'comment': "Table of chosen transaction tags"
    }

    transaction_hash_id = Column(
        VARCHAR,
        ForeignKey('financial_transaction.hash_id', ondelete='CASCADE')
    )
    tag_id = Column(
        Integer,
        ForeignKey('financial_tag.id', ondelete='CASCADE')
    )

    transaction = relationship(
        "FinancialTransaction",
        lazy='selectin',
        foreign_keys=[transaction_hash_id],
        back_populates="transactions_tags"
    )
    tag = relationship(
        "FinancialTag",
        lazy='selectin',
        foreign_keys=[tag_id],
        uselist=False
    )

    def __repr__(self):
        return f"TransactionTag of {self.transaction_hash_id} | ID: {self.id}"
