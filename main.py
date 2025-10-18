import  requests
from bs4 import BeautifulSoup
import json

URL = "https://asaxiy.uz/"
HOST = "https://asaxiy.uz"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}


def get_soup(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_category():
    soup = get_soup(URL)
    bar = soup.find("nav", class_="header__nav")
    products = bar.find_all("a", class_="header__nav__link")
    data = [
        {
            "title": product.text.strip(),
            "link": HOST + product.get("href"),
        }
        for product in products
    ]
    return data


# print(get_category())


def get_description(link):
    print(link)
    soup = get_soup(link)
    table = soup.find("table", class_="table table-striped table-borderless")
    if not table:
        return None

    products = table.find_all("tr")
    if not products:
        return None

    data = []
    for product in products:
        n1 = product.find("td", class_="text-left").text.strip()
        n2 = product.find("td", class_="text-right res--custom-link").text.strip()
        data.append({n1: n2})
    return data

def get_reviews(link):
    print(link)
    soup = get_soup(link)
    all = soup.find("div", class_="feedback")
    if not all:
        return None
    reviews = all.find_all("div", class_="feedback__item")
    if not reviews:
        return None

    data = []
    for product in reviews:
        n1 = product.find("div", class_="feedback__user").find("span").text.strip()
        n2 = product.find("p", class_="feed__text").text.strip()
        data.append({n1: n2})
    return data




def get_products(link):
    soup = get_soup(link)
    all = soup.find("div", class_="row custom-gutter mb-40")
    products = all.find_all("div", class_="col-6 col-xl-3 col-md-4")
    data = [
        {
            "title": product.find("p", class_="title__link").text.strip(),
            "price": product.find("div", class_="produrct__item-prices--wrapper").find_all("span")[-1].text.strip(),
            "img": product.find("img", class_="img-fluid lazyload").get("data-src"),
            "link": HOST + product.select_one('a[onclick="selectItemGtag()"]').get("href"),
            "description": get_description(HOST + product.select_one('a[onclick="selectItemGtag()"]').get("href")),
            "Reviews": get_reviews(HOST + product.select_one('a[onclick="selectItemGtag()"]').get("href"))

        }
        for product in products
    ]
    return data





























def main():
    data = get_category()
    for product in data:
        product["products"] = get_products(product["link"])

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()


