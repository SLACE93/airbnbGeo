import scrapy
from airbnbScrapy.items import AirbnbItem
from scrapy.loader import ItemLoader

class AirbnbSpider(scrapy.Spider):
    name = 'AirbnbSP'
    start_urls = ['https://www.airbnb.com/s/New-York--NY', 'https://www.airbnb.com/s/Paris--France', 'https://www.airbnb.com/s/Hawaii--United-States',
                  'https://www.airbnb.com/s/Barcelona--Spain', 'https://www.airbnb.com/s/London--United-Kingdom', 'https://www.airbnb.com/s/San-Francisco--CA',
                  'https://www.airbnb.com/s/Berlin--Germany', 'https://www.airbnb.com/s/Budapest--Hungary', 'https://www.airbnb.com/s/Rio-de-Janeiro',
                  'https://www.airbnb.com/s/Austin', 'https://www.airbnb.com/s/Miami', 'https://www.airbnb.com/s/Rome',
                  'https://www.airbnb.com/s/Venice', 'https://www.airbnb.com/s/Washington-DC', 'https://www.airbnb.com/s/Sydney']

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        paginas = sel.xpath('//div[@class="pagination pagination-responsive"]/ul/li')
        paginas = paginas.xpath('.//a/@target')
        paginas_link = paginas.extract()
        size =  len(paginas_link)
        #pag_inicial = int(paginas_link[0])
        pag_final = int(paginas_link[size-2])
        control = 1
        pageConcat = '?page='
        while control <= pag_final:
            full_url = response.url + pageConcat + str(control)
            control += 1
            yield scrapy.Request(full_url, callback=self.parse_link_rooms)

    def parse_link_rooms(self, response):
        sel = scrapy.selector.Selector(response)
        rooms = sel.xpath('//div[@class="search-results"]/div/div/div')
        for room in rooms:
            dptolinks =  room.xpath('.//a[@class="media-photo media-cover"]/@href')
            for href in dptolinks:
                full_url = 'https://www.airbnb.com' + href.extract()
                yield scrapy.Request(full_url, callback=self.parse_room)

    def parse_room(self, response):
        sel = scrapy.selector.Selector(response)
        l = ItemLoader(AirbnbItem(), sel)
        latitude = sel.xpath('//meta[@property="airbedandbreakfast:location:latitude"]/@content').extract_first()
        longitude = sel.xpath('//meta[@property="airbedandbreakfast:location:longitude"]/@content').extract_first()
        coord = latitude + '&' + longitude
        neighbor =  sel.xpath('//div[@class="h3"]/a[@class="link-reset"]/text()').extract_first()
        #city = sel.xpath('//div[@id="display-address"]/a/text()').extract_first()
        l.add_xpath('nombreVenue', '//h1[@id="listing_name"]/text()')
        l.add_xpath('city', '//div[@id="display-address"]/a/text()')
        l.add_value('coordenadas', coord)
        l.add_xpath('total_visitas', '//div[@class="review-wrapper"]/div/div/h4/span/text()')
        l.add_xpath('score_prom', '//div[@class="review-wrapper"]/div/div/h4/span/text()')
        l.add_xpath('nums_evaluacion', '//div[@class="review-wrapper"]/div/div/h4/span/text()')
        l.add_xpath('categoria', '//a[@class="link-reset"]/strong/text()')
        l.add_xpath('precios', '//a[@id="cancellation-policy"]/strong/text()')
        #l.add_xpath('neighborhood', '//div[@class="col-8 col-offset-2 col-middle"]/div[@class="h3"]/a[@class="link-reset"]/text()')
        yield l.load_item()
