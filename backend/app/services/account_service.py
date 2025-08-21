from typing import List, Optional
from bson import ObjectId
from ..db import get_database
from ..models.account import AccountCreate, AccountInDB
from ..core.security import encrypt_password

COLLECTION_NAME = "accounts"

async def create_account(account_data: AccountCreate) -> AccountInDB:
    """
    Creates a new account document in the database.
    """
    db = get_database()
    collection = db[COLLECTION_NAME]

    hashed_password = encrypt_password(account_data.password)

    account_in_db = AccountInDB(
        username=account_data.username,
        hashed_password=hashed_password
    )

    insert_data = account_in_db.model_dump(by_alias=True, exclude={"id"})

    result = await collection.insert_one(insert_data)

    created_account = await collection.find_one({"_id": result.inserted_id})

    return AccountInDB(**created_account)

async def get_all_accounts() -> List[AccountInDB]:
    """
    Retrieves all accounts from the database.
    """
    db = get_database()
    collection = db[COLLECTION_NAME]
    accounts = []
    cursor = collection.find()
    async for document in cursor:
        accounts.append(AccountInDB(**document))
    return accounts

async def get_account_by_id(account_id: str) -> Optional[AccountInDB]:
    """
    Retrieves a single account by its ID.
    """
    if not ObjectId.is_valid(account_id):
        return None
    db = get_database()
    collection = db[COLLECTION_NAME]
    account = await collection.find_one({"_id": ObjectId(account_id)})
    if account:
        return AccountInDB(**account)
    return None

async def delete_account(account_id: str) -> bool:
    """
    Deletes an account from the database by its ID.
    """
    if not ObjectId.is_valid(account_id):
        return False
    db = get_database()
    collection = db[COLLECTION_NAME]
    result = await collection.delete_one({"_id": ObjectId(account_id)})
    return result.deleted_count > 0
