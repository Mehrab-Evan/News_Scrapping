from pydantic import BaseModel

class NewsBase(BaseModel):
    pass

class NewsUrl(NewsBase):
    news_link: str

class NewsCreate(NewsBase):
    title: str
    reporter: str
    publisher: str
    news_datetime: str
    category: str
    news_content: str
    news_link: str

class NewsView(NewsBase):
    id: int
    title: str
    reporter: str
    news_datetime: str
    news_content: str
    news_link: str
    category: str
    publisher: str

class NewsUpdate(NewsBase):
    title: str
    reporter: str
    news_datetime: str
    news_content: str
    news_link: str
    news_image: str
    category: str
    publisher: str

class NewsDelete(NewsBase):
    id: int
