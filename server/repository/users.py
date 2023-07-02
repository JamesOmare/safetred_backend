from sqlalchemy.orm import Session
from sqlalchemy import update as sql_update
from model.users import Users
from schemas.user import UserCreate
from sqlalchemy.future import select
from typing import Optional
from security import get_password_hash, verify_password

async def commit_rollback(db: Session):
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
class UserRepo:
    
    async def create(db: Session, user: Users):
            db_user = Users(
                email=user.email,
                username=user.username,
                password= get_password_hash(user.password),
                phone_number=user.phone_number,
                is_active=user.is_active,
                is_superuser=user.is_superuser
                )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        
    def get_user_by_id(db: Session,_id):
        return db.query(Users).filter(Users.id == _id).first()
    
    def get_user_by_email(db: Session, email):
        return db.query(Users).filter(Users.email == email).first()

    async def find_by_username(db: Session, username: str):
        query = select(Users).where(Users.username == username)
        return db.execute(query).scalar_one_or_none()
    
    def fetch_by_username(db: Session, username:str):
        return db.query(Users).filter(Users.username == username).first()
    
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Users).offset(skip).limit(limit).all()
    
    async def delete(db: Session, user_id):
        db_user= db.query(Users).filter_by(id=user_id).first()
        db.delete(db_user)
        db.commit()
        
    async def fetch_user_by_email(email: str) -> Optional[Users]:
        user = await Users.find_one(Users.email == email)
        return user
    
    # async def get_user_by_id(id: UUID) -> Optional[User]:
    #     user = await User.find_one(User.user_id == id)
    #     return user
    
    async def update_password(db: Session, email: str, password: str):
        query = sql_update(Users).where(Users.email == email).values(
            password=password).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()
        
        
    async def update(db: Session,user_data):
        updated_item = db.merge(user_data)
        db.commit()
        return updated_item

# class ItemRepo:
    
#  async def create(db: Session, item: schemas.ItemCreate):
#         db_item = models.Item(name=item.name,price=item.price,description=item.description,store_id=item.store_id)
#         db.add(db_item)
#         db.commit()
#         db.refresh(db_item)
#         return db_item
    
#  def fetch_by_id(db: Session,_id):
#      return db.query(models.Item).filter(models.Item.id == _id).first()
 
#  def fetch_by_name(db: Session,name):
#      return db.query(models.Item).filter(models.Item.name == name).first()
 
#  def fetch_all(db: Session, skip: int = 0, limit: int = 100):
#      return db.query(models.Item).offset(skip).limit(limit).all()
 
#  async def delete(db: Session,item_id):
#      db_item= db.query(models.Item).filter_by(id=item_id).first()
#      db.delete(db_item)
#      db.commit()
     
     
#  async def update(db: Session,item_data):
#     updated_item = db.merge(item_data)
#     db.commit()
#     return updated_item
    
    
    
# class StoreRepo:
    
#     async def create(db: Session, store: schemas.StoreCreate):
#             db_store = models.Store(name=store.name)
#             db.add(db_store)
#             db.commit()
#             db.refresh(db_store)
#             return db_store
        
#     def fetch_by_id(db: Session,_id:int):
#         return db.query(models.Store).filter(models.Store.id == _id).first()
    
#     def fetch_by_name(db: Session,name:str):
#         return db.query(models.Store).filter(models.Store.name == name).first()
    
#     def fetch_all(db: Session, skip: int = 0, limit: int = 100):
#         return db.query(models.Store).offset(skip).limit(limit).all()
    
#     async def delete(db: Session,_id:int):
#         db_store= db.query(models.Store).filter_by(id=_id).first()
#         db.delete(db_store)
#         db.commit()
        
#     async def update(db: Session,store_data):
#         db.merge(store_data)
#         db.commit()