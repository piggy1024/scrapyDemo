# -*- coding: utf-8 -*-


from scrapy import cmdline


name = 'douban_ajax'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())