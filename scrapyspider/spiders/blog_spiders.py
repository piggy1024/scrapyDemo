from scrapy.spiders import Spider


class BlogSpider(Spider):
    name = 'woodenrobot'
    start_urls = ['https://movie.douban.com/']

    def parse(self, response):
        titles = response.xpath('//a[@class="item"]/p/text()').extract()
        for title in titles:
            print(title.strip())

