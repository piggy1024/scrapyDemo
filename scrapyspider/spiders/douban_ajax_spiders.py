# -*- coding: utf-8 -*-
import json
import re

from scrapy import Request, Spider

from scrapyspider.items import DoubanMovieAjaxItem


class DoubanAjaxSpider(Spider):
    name = 'douban_ajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=0&genres=%E5%8A%A8%E4%BD%9C'
        yield Request(url, headers = self.headers)

    def parse(self, response):
        datas = json.loads(response.body)
        # 因为返回的内容是   {data: content}  所以需要将content取出
        datas = datas['data']
        item = DoubanMovieAjaxItem()
        if datas:
            for data in datas:
                item['score'] = data['rate']
                item['movie_name'] = data['title']
                item['id'] = data['id']
                item['star'] = data['star']
                yield item

                # 如果datas存在数据则对下一页进行采集
                page_num = re.search(r'start=(\d+)', response.url).group(1)
                page_num = 'start=' + str(int(page_num)+20)
                next_url = re.sub(r'start=\d+', page_num, response.url)
                yield Request(next_url, headers = self.headers)

