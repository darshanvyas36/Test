from fastapi import APIRouter, HTTPException, status
from typing import List
from ..services import account_service
from ..models.account import AccountCreate, AccountPublic

router = APIRouter()

@router.post(
    "/",
    response_model=AccountPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new Instagram account"
)
async def create_new_account(account: AccountCreate):
    """
    Endpoint to add a new Instagram account.
    """
    created_account = await account_service.create_account(account)
    return created_account

@router.get(
    "/",
    response_model=List[AccountPublic],
    summary="List all managed Instagram accounts"
)
async def get_all_accounts():
    """
    Endpoint to retrieve all managed accounts.
    """
    accounts_in_db = await account_service.get_all_accounts()
    return [AccountPublic.model_validate(acc.model_dump(by_alias=True)) for acc in accounts_in_db]

@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a managed Instagram account"
)
async def delete_account_by_id(account_id: str):
    """
    Endpoint to delete a specific account.
    """
    account = await account_service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found."
        )

    deleted = await account_service.delete_account(account_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete account with ID {account_id}."
        )

    return
