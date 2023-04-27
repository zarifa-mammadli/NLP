import scrapy
from datetime import datetime

class BloombergSitemapSpider(scrapy.Spider):
    name = 'sp_project'
    allowed_domains = ['bloomberg.com']
    #start_urls = ['https://www.bloomberg.com/feeds/bbiz/sitemap_2010_3.xml']
    def start_requests(self):
       # Generate URLs for all sitemaps for all years and months
       base_url = 'https://www.bloomberg.com/feeds/bbiz/sitemap_{}_{}.xml'
       start_year = 2010
       end_year = datetime.now().year
       for year in range(start_year, end_year+1):
           for month in range(1, 13):
               url = base_url.format(year, month)
               yield scrapy.Request(url, self.parse)
           
    def parse(self, response):
        loc=response.xpath('//sitemap:loc/text()', namespaces={'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}).extract()
        lastmod=response.xpath('//sitemap:lastmod/text()', namespaces={'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}).extract()
        changefreq =response.xpath('//sitemap:changefreq/text()', namespaces={'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}).extract()
        priority = response.xpath('//sitemap:priority/text()', namespaces={'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}).extract()
        
        for loc, lastmod, changefreq, priority in zip(loc, lastmod, changefreq, priority):
            yield {'Locs': loc, 'Lastmod': lastmod, 'Changefreq': changefreq, 'Priority':priority,'URL':response.url}

