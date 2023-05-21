import multiprocessing

import scrapy
from scrapy.crawler import CrawlerProcess

import diy_bbt.providers.utils.sub_parsers as sp


# Spider process
class CustomSpider(scrapy.Spider):
    def __init__(self, url, sub_parse, result_queue):
        super().__init__()
        self.start_urls = [url]
        self.sub_parse = sub_parse
        self.result_queue = result_queue

    name = "custom_spider"

    def parse(self, response):
        result = self.sub_parse(response)
        self.result_queue.put(result)


def run_spider_worker(url, sub_parse, result_queue):
    process = CrawlerProcess(
        {
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
            "LOG_ENABLED": False,
        }
    )

    process.crawl(CustomSpider, url=url, sub_parse=sub_parse, result_queue=result_queue)
    process.start(stop_after_crawl=True)


def run_spider(url, sub_parse):
    result_queue = multiprocessing.Queue()
    worker_process = multiprocessing.Process(
        target=run_spider_worker, args=(url, sub_parse, result_queue)
    )
    worker_process.start()
    worker_process.join()
    return result_queue.get()


# Command functions
def commodities_elec():
    return run_spider("https://tradingeconomics.com/commodities", sp.commodities_elec)


def commodities_indices():
    return run_spider(
        "https://tradingeconomics.com/commodities", sp.commodities_indices
    )


def macro_industry():
    return run_spider(
        "https://finviz.com/groups.ashx?g=industry&v=110&o=-marketcap",
        sp.macro_industry,
    )


def macro_sector():
    return run_spider(
        "https://finviz.com/groups.ashx?g=sector&v=110&o=-marketcap",
        sp.macro_sector,
    )


def misc_insider():
    return run_spider("https://finviz.com/insidertrading.ashx", sp.macro_insider)
