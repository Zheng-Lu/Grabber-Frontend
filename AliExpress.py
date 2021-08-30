import os
import execjs
import requests
import random
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask import request, redirect, url_for

app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods={"POST", "GET"})
def search():
    if request.method == "POST":
        # Get selected platform from user
        Platform = request.form.get('Platforms')
        StoreID = request.form.get('StoreID')
        numPages = request.form.get('numPages')
        sortType = request.form.get('sortTypes')
        return Platform, StoreID, numPages, sortType
    else:
        print("Nothing")
        return None



if __name__ == '__main__':
    app.run(debug=True)


user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

AliExpress_headers = {
    'user-agent': random.choice(user_agent_list),
}


def js_from_file(file_name):
    """
    reading javascript file
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()

    return result


js_code = execjs.compile(js_from_file("./AliSliderCracker.js"))


def downloadSourceCode():
    urls = []
    requests_result = []

    numPages = int(input('Number of pages you want to scrape: '))
    choice = int(input(
        "Sort Types:\n1.Best Match    2.Price \u2193    3.Price \u2191    4.New \u2193     5.Orders \u2193\nChoose one of Sort Types above:"))

    while choice not in [x for x in range(1, 6)]:
        print("Out of range! Choose between 1 ~ 5")
        choice = int(input(
            "Sort Types:\n1.Best Match    2.Price \u2193    3.Price \u2191    4.New \u2193     5.Orders \u2193\nChoose one of Sort Types above:"))

    sort_types = {1: 'bestmatch_sort', 2: 'price_desc', 3: 'price_asc', 4: 'new_desc', 5: 'orders_desc'}

    search_text = input("Input key word to search specific products(Press [Enter\u23CE] to ignore) : ")

    for i in range(1, numPages + 1):
        urls.append("https://www.aliexpress.com/store/sale-items/" + str(store_id) + '/' + str(
            i) + f".html?origin=n&promotionType=fixed&SortType={sort_types[choice]}&SearchText={search_text}")

    for url in urls:
        req_result = requests.get(url, 'html.parser').text
        if 'pic-rind' not in req_result:
            js_code.call("bypass", url)
        else:
            requests_result.append(req_result)

    return requests_result


def readData():
    IDlist = []
    with open("productId.txt", "r") as f:
        for line in f:
            products = line.split(",")
            for product in products:
                IDlist.append(product.replace("'", ""))
    return IDlist


def downloadProductSrc(IDlist):
    urls_list = []

    for ID in IDlist:
        urls_list.append("https://www.aliexpress.com/item/" + ID + ".html")

    return urls_list


def getProductURL(requests_result):
    """
    :param requests_result:
    :return:
    """
    urls_list = []
    for srcPerPage in requests_result:
        soup = BeautifulSoup(srcPerPage, 'html.parser')
        urls_list.append(soup.findAll('a', {'class': 'pic-rind'}))

    for urls in urls_list:
        for i in range(len(urls)):
            urls[i] = 'https:' + urls[i].get('href')

    return urls_list


def download_product(urls_list):
    # Example of path: C://Users//Lenovo//Desktop//html//911651019//
    parent_dir = input("Enter the path you wanna store your HTML files: ")
    folder_name = str(store_id)
    path = os.path.join(parent_dir, folder_name)
    os.mkdir(path)

    for urls in urls_list:
        for url in urls:
            try:
                response = requests.get(url, headers=AliExpress_headers)
                content = response.content
            except:
                response = requests.get(url, headers=AliExpress_headers)
                js_code.call("bypass", url)
                content = response.content

            product_id = (url.split('.html')[0]).split('/item/')[1]
            file_name = product_id + '.html'
            with open(os.path.join(path, file_name), 'wb') as f:
                f.write(content)

    # for url in urls_list:
    #     try:
    #         response = requests.get(url, headers=AliExpress_headers)
    #         content = response.content
    #
    #     except:
    #         response = requests.get(url, headers=AliExpress_headers)
    #         js_code.call("bypass", url)
    #         content = response.content
    #
    #     product_id = (url.split('.html')[0]).split('/item/')[1]
    #     file_name = product_id + '.html'
    #     with open(os.path.join(path, file_name), 'wb') as f:
    #         f.write(content)


def run():
    srcCode = downloadSourceCode()
    print(srcCode)
    urls = getProductURL(srcCode)
    print(urls)
    download_product(urls)


if __name__ == '__main__':
    store_id = int(input('Store ID to grab source from: '))
    run()

    # Download from text file
    # url_list = downloadProductSrc(readData())
    # download_product(url_list)
