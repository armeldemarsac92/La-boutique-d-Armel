from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.exc import SQLAlchemyError


Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    item_title = Column(String)
    item_picture = Column(String)
    item_link = Column(String)
    item_color = Column(String)
    item_price = Column(Float)
    item_description = Column(String)
    item_size = Column(String)
    item_brand = Column(String)
    item_initial_views = Column(Integer)
    item_current_views = Column(Integer)
    item_initial_followers = Column(Integer)
    item_current_followers = Column(Integer)
    item_location = Column(String)
    item_date_added = Column(DateTime)
    date_scrapped = Column(DateTime)
    query = Column(String)
    session_token = Column(String)
    raindrop_collection = Column(String)
    raindrop_collection_id = Column(Integer)
    status = Column(String)


class DatabaseHandler:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def item_exists(self, item_link):
        return self.session.query(exists().where(Item.item_link == item_link)).scalar()

    def add_item(self, item):
        try:
            self.session.add(item)
            self.session.commit()
        except SQLAlchemyError as e:
            print("Error inserting item data into the PostgreSQL database:", e)

