# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import DoubanMovieItem


class DoubanMovieTop250Spider(Spider):
    name = "douban250"
    start_urls = ["https://movie.douban.com/top250"]
    headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    # allowed_domains
    # 可选。包含了spider允许爬取的域名(domain)列表(list)。 当OffsiteMiddleware启用时， 域名不在列表中的URL不会被跟进。

    # start_urls
    # URL列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。 因此，第一个被获取到的页面的URL将是该列表之一。 后续的URL将会从获取到的数据中提取。

    # start_requests()
    # 该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request。
    # 如果您想要修改最初爬取某个网站的Request对象，您可以重写(override)
    # 该方法。 例如，如果您需要在启动时以POST登录某个网站，你可以这么写:
    # def start_requests(self):
    #     return [scrapy.FormRequest("http://www.example.com/login",
    #                                formdata={'user': 'john', 'pass': 'secret'},
    #                                callback=self.logged_in)]
    #
    # def logged_in(self, response):
    #     # here you would extract links to follow and return Requests for
    #     # each of them, with another callback
    #     pass

    def start_requests(self):
        # url = "https://movie.douban.com/top250"
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers = self.headers)

    def parse(self, response):
        item = DoubanMovieItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['score_number'] = movie.xpath(
                './/div[@class="star"]/span/text()').re(u'(\d+)人评价')[0]
            yield item
        # 如果有下一页
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers= self.headers)
