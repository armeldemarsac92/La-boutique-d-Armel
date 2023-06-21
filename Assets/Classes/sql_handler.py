from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, exists
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base


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

    def __init__(self, item_data):
        self.item_title = item_data.get("title")
        self.item_picture = item_data.get("item_picture")
        self.item_link = item_data.get("item_link")
        self.item_color = item_data.get("color")
        self.item_price = item_data.get("price")
        self.item_description = item_data.get("description")
        self.item_size = item_data.get("size")
        self.item_brand = item_data.get("brand")
        self.item_initial_views = item_data.get("views")
        self.item_current_views = item_data.get("views")
        self.item_initial_followers = item_data.get("followers")
        self.item_current_followers = item_data.get("followers")
        self.item_location = item_data.get("location")
        self.item_date_added = item_data.get("date_added")
        self.date_scrapped = item_data.get("date_scrapped")
        self.query = item_data.get("query")
        self.session_token = item_data.get("session_token")
        self.raindrop_collection = item_data.get("raindrop_collection")
        self.raindrop_collection_id = item_data.get("raindrop_collection_id")
        self.status = item_data.get("status")



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

