# news table
from sqlalchemy import Column, Integer, String
from database import Base

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    reporter = Column(String, index=True)
    news_datetime = Column(String, index=True)
    news_content = Column(String, index=True)
    news_link = Column(String, index=True)
    news_image = Column(String, index=True)
    category = Column(String, index=True)
    publisher = Column(String, index=True)
