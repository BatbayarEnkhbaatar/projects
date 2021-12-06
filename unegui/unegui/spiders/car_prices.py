import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CarPricesSpider(CrawlSpider):
    name = 'car_prices'
    allowed_domains = ['www.unegui.mn']
    start_urls = ['http://www.unegui.mn/avto-mashin/-avtomashin-zarna']
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='announcement-container']/a"), callback='parse_item',follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='number-list-next js-page-filter number-list-line']"))
    )

    def parse(self, response):
        yield {
            'title': response.xpath("normalize-space(//div[@class='announcement-content-header']/h1[@class='title-announcement']/text())").get(),
            'made_year': response.xpath("//div[@class='announcement-characteristics clearfix']/ul[@class='chars-column']/li[6]/a/text()").get(),
            'imported_year': response.xpath("//div[@class='announcement-characteristics clearfix']/ul[@class='chars-column']/li[7]/a/text()").get(),
            'price': response.xpath("//div[@class='announcement-price__cost']/meta[@itemprop='price']/@content").get(),
            'date': response.xpath("//div[@class='announcement__details ']/span[1]/text()").get()
        }


