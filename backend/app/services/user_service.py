from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import UserUpdate
from app.core.security import hash_password


# =====================================================
# Create User
# =====================================================

def create_user(db: Session, user: UserCreate):

    existing = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing:
        raise Exception("Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =====================================================
# Get All Users
# =====================================================

def get_all_users(db: Session):
    return db.query(User).all()


# =====================================================
# Get User By ID
# =====================================================

def get_user_by_id(
    db: Session,
    user_id: int,
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# =====================================================
# Update User
# =====================================================

def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
):

    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


# =====================================================
# Soft Delete User
# =====================================================

def soft_delete_user(
    db: Session,
    user_id: int,
):

    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    user.is_active = False

    db.commit()
    db.refresh(user)

    return user


# =====================================================
# Restore User
# =====================================================

def restore_user(
    db: Session,
    user_id: int,
):

    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    user.is_active = True

    db.commit()
    db.refresh(user)

    return user


# =====================================================
# Activate User
# =====================================================

def activate_user(
    db: Session,
    user_id: int,
):

    return restore_user(db, user_id)


# =====================================================
# Deactivate User
# =====================================================

def deactivate_user(
    db: Session,
    user_id: int,
):

    return soft_delete_user(db, user_id)


# =====================================================
# Assign Role
# =====================================================

def assign_role(
    db: Session,
    user_id: int,
    role: str,
):

    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    user.role = role

    db.commit()
    db.refresh(user)

    return user


# =====================================================
# Search Users
# =====================================================

def search_users(
    db: Session,
    keyword: str,
):

    return (
        db.query(User)
        .filter(
            or_(
                User.name.ilike(f"%{keyword}%"),
                User.email.ilike(f"%{keyword}%"),
                User.role.ilike(f"%{keyword}%"),
            )
        )
        .all()
    )


# =====================================================
# Pagination
# =====================================================

def get_users_paginated(
    db: Session,
    page: int = 1,
    page_size: int = 10,
):

    offset = (page - 1) * page_size

    total = db.query(func.count(User.id)).scalar()

    users = (
        db.query(User)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "page": page,
        "page_size": page_size,
        "total_users": total,
        "total_pages": (
            (total + page_size - 1) // page_size
            if total
            else 0
        ),
        "users": users,
    }


# =====================================================
# User Statistics
# =====================================================

def get_user_statistics(
    db: Session,
):

    total_users = db.query(func.count(User.id)).scalar()

    active_users = (
        db.query(func.count(User.id))
        .filter(User.is_active == True)
        .scalar()
    )

    inactive_users = (
        db.query(func.count(User.id))
        .filter(User.is_active == False)
        .scalar()
    )

    admin_count = (
        db.query(func.count(User.id))
        .filter(User.role == "admin")
        .scalar()
    )

    safety_officer_count = (
        db.query(func.count(User.id))
        .filter(User.role == "safety_officer")
        .scalar()
    )

    worker_count = (
        db.query(func.count(User.id))
        .filter(User.role == "worker")
        .scalar()
    )

    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "admins": admin_count,
        "safety_officers": safety_officer_count,
        "workers": worker_count,
    }


# =====================================================
# Admin Dashboard Statistics
# =====================================================

def get_admin_dashboard_statistics(
    db: Session,
):

    return {
        "user_statistics": get_user_statistics(db),
        "recent_users": (
            db.query(User)
            .order_by(User.created_at.desc())
            .limit(5)
            .all()
        ),
    }