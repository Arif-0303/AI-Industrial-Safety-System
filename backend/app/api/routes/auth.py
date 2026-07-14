from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User

from app.schemas.auth import (
    UserRegister,
    UserResponse,
    UserLogin,
    TokenResponse,
    UserUpdate,
)

from app.core.security import hash_password
from app.core.auth import (
    get_current_user,
    require_admin,
    require_safety_officer,
    require_worker,
)

from app.services.auth_service import authenticate_user
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    soft_delete_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =====================================================
# Register
# =====================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )

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
# Login
# =====================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return authenticate_user(
        user.email,
        user.password,
        db,
    )


# =====================================================
# Current Logged-in User
# =====================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


# =====================================================
# RBAC Test APIs
# =====================================================

@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_admin),
):
    return {
        "message": "Welcome Admin",
        "user": current_user.name,
    }


@router.get("/safety-test")
def safety_test(
    current_user: User = Depends(require_safety_officer),
):
    return {
        "message": "Welcome Safety Officer",
        "user": current_user.name,
    }


@router.get("/worker-test")
def worker_test(
    current_user: User = Depends(require_worker),
):
    return {
        "message": "Welcome Worker",
        "user": current_user.name,
    }


# =====================================================
# Get All Users (Admin Only)
# =====================================================

@router.get(
    "/users",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_all_users(db)


# =====================================================
# Get User By ID (Admin Only)
# =====================================================

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


# =====================================================
# Update User (Admin Only)
# =====================================================

@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
)
def update_user_api(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    updated_user = update_user(
        db,
        user_id,
        user,
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return updated_user


# =====================================================
# Soft Delete User (Admin Only)
# =====================================================

@router.delete(
    "/users/{user_id}",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = soft_delete_user(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User deactivated successfully."
    }