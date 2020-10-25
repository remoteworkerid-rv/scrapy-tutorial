from typing import List

import scrapy
from cssselect import Selector

class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['0.0.0.0']

    # REQUEST LOGIN DARI URLS
    start_urls = ['http://0.0.0.0:9999/']

    # LOGIN DISINI
    def parse(self, response):
        # apa bedanya yield & return
        # yield {"title": response.css("title::text").get()}

        # cek di inspect element perlu login tidak?

        data = {
            "username": "user",
            "password": "user12345"
        }

        # cek di FormRequest butuhnya apa aja
        return scrapy.FormRequest(
            url="http://0.0.0.0:9999/login",
            formdata=data,
            callback=self.after_login            # untuk mengektraksi data
        )

    def after_login(self, response):
        """
        Ada 2 Task disini :
        1. Ambil semua data barang yang ada dihalaman hasil -> akan menuju detail (parsing detail)
        2. Ambil semua link next -> akan balik ke self.after_login

        :param response:
        :return:
        """

        # get detail product
        detail_products: List[Selector] = response.css(".card .card-title a")
        for detail in detail_products:
            href = detail.attrib.get("href")         # untuk mendapatkan urls
            yield response.follow(href, callback=self.parse_detail)         # masukkan urls ini ke antrian scrapy

        yield {"title": response.css("title::text").get()}

    def parse_detail(self, response):
        yield {"title": response.css("title::text").get()}
