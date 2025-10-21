from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from src.models.Item import Item
from src.models.User import User


class ItemService:

    @staticmethod
    def get_all(db: Session, query: dict = None):
        q = db.query(Item)
        if query and 'name' in query:
            q = q.filter(Item.name.ilike(f"%{query['name']}%"))
        return q.all()

    @staticmethod
    def create(db: Session, data: dict, owner_id: int):
        item = Item(**data, owner_id=owner_id)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def remove(db: Session, item_id: int):
        item = db.query(Item).get(item_id)
        if item:
            db.delete(item)
            db.commit()
        return item

    @staticmethod
    def get_item(db: Session, item_id: int):
        return db.query(Item).get(item_id)

    @staticmethod
    def edit(db: Session, item_id: int, data: dict):
        item = db.query(Item).get(item_id)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            db.commit()
            db.refresh(item)
        return item

    @staticmethod
    def get_by_id(db: Session, item_id: int):
        return db.query(Item).options(joinedload(Item.userList)).get(item_id)

    @staticmethod
    def like(db: Session, item_id: int, user_id: int):
        item = db.query(Item).get(item_id)
        user = db.query(User).get(user_id)
        if item and user and user not in item.userList:
            item.userList.append(user)
            db.commit()
            db.refresh(item)
        return item

    # @staticmethod
    # def search(db: Session, query: dict = None):
    #     q = db.query(Item)
    #     if query:
    #         if 'name' in query:
    #             q = q.filter(Item.name.ilike(f"%{query['name']}%"))
    #         if 'category' in query:
    #             q = q.filter(Item.category.ilike(f"%{query['category']}%"))
    #     return q.all()
