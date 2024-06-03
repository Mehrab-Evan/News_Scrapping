from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schema.news_scrapper import NewsCreate, NewsView, NewsUpdate, NewsDelete, NewsUrl
from crud import news_scrapper_crud
from database import SessionLocal
import httpx
from pyppeteer import launch
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time
router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def render_page(url: str):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForTimeout(3000)  # Waiting for the page to fully render
    content = await page.content()
    await browser.close()
    return content

@router.post("/new_news", response_model=NewsCreate)
async def create_news(news: NewsUrl, db: Session = Depends(get_db)):
    try:
        url = news.news_link
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            html_content = response.text

        # print(html_content)

        # find title from html content
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('title').text
        # print(title)

        # find .contributor-name from html content
        reporter = soup.find('span', class_='contributor-name').text
        # print(reporter)

        # print(response.html.html)
        publisher_website = url.split('/')[2]       
        publisher = publisher_website.split('.')[-2]  
        # print(publisher)

        # find datetime from html content
        datetime_element = soup.find('time')
        news_datetime = datetime_element['datetime']
        # print(news_datetime)
        # print(type(news_datetime))

        # find category from .print-entity-section-wrapper
        category = soup.find(class_='print-entity-section-wrapper').text
        # print(category)

        # find news body from p tags
        news_content = soup.find('div')
        news_body = news_content.find_all('p')
        news_body = '\n'.join([p.text for p in news_body])
        # print(news_body)

        time.sleep(5)    
        # Extract image URL
        session = HTMLSession()
        response = session.get(url)
        img_tags = response.html.find('img')
        print(img_tags)
        # images = '\n'.join([img.attrs['src'] for img in img_tags if 'src' in img.attrs])
        # print(images)
        images = []
        for img_tag in img_tags:
            if img_tag:
                img_url = img_tag.attrs['src']
                images.append(img_url)
                print(f"Image URL: {img_url}")
            else:
                print("No image tag found.")
        # insert into news_scrapper_crud if not exists
        does_news_exist = news_scrapper_crud.get_news_by_link(db, news_link=url)
        if does_news_exist:
            return does_news_exist
        else:\
            return news_scrapper_crud.create_news(db, NewsCreate(title=title, reporter=reporter, news_datetime=news_datetime, news_content=news_body, news_link=url, category=category, publisher=publisher))

        # return NewsCreate(title=title, reporter=reporter, news_datetime=news_datetime, news_content=news_body, news_link=url, category=category, publisher=publisher)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the news article")
 
    finally:
        # Close the session if any
        pass

@router.get("/all_news", response_model=list[NewsView])
def get_all_news(db: Session = Depends(get_db)):
    return news_scrapper_crud.get_all_news(db)
