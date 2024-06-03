from sqlalchemy.orm import Session
from model.news import News
from schema.news_scrapper import NewsCreate, NewsView, NewsUpdate, NewsDelete

def create_news(db: Session, news: NewsCreate):
    # if news already exists, return the news
    db_news = db.query(News).filter(News.news_link == news.news_link).first()
    if db_news:
        return db_news
    db_news = News(title=news.title, reporter=news.reporter, news_datetime=news.news_datetime, news_content=news.news_content, news_link=news.news_link, category=news.category, publisher=news.publisher)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def get_all_news(db: Session):
    return db.query(News).all()

def get_news_by_id(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()

def get_news_by_link(db: Session, news_link: str):
    return db.query(News).filter(News.news_link == news_link).first()

def get_news_by_reporter(db: Session, reporter: str):
    return db.query(News).filter(News.reporter == reporter).all()

def news_delete(db: Session, news_id: int):
    db.query(News).filter(News.id == news_id).delete()
    db.commit()
    return {"message": "News deleted successfully"}
