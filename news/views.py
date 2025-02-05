
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup as BSoup
from django.shortcuts import redirect
from .models import Headline


def scrape(request, name):
    Headline.objects.all().delete()

    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://www.theonion.com/{name}"

    response = session.get(url)
    soup = BSoup(response.content, "html.parser")


    articles = soup.select("article")

    for article in articles:
        try:

            link_tag = article.select_one("a[href]")
            link = link_tag["href"] if link_tag else None


            title_tag = article.select_one("h2")
            title = title_tag.text.strip() if title_tag else "No Title"


            img_tag = article.select_one("img")
            img_url = img_tag["src"] if img_tag else None


            if link and title:
                new_headline = Headline(title=title, url=link, image=img_url)
                new_headline.save()

        except Exception as e:
            print(f"Error processing article: {e}")

    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "news/home.html", context)
