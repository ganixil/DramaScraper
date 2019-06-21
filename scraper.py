import scrapy

class MeijuSetSpider(scrapy.Spider):
        name = "meiju_spider"

        #the website you want to scrap
        start_urls = ['https://91mjw.com/category/all_mj']
    
        def parse(self, response):
                SET_SELECTOR = '.u-movie'
                for movie in response.css(SET_SELECTOR)[:-3]:
                    #selector specify for which attribute
                    NAME_SELECTOR = 'a ::attr(title)'
                    RATING_SELECTOR = './div[1]/span/text()'
                    STATUS_SELECTOR = './div[2]/span/text()'
                    GENRE_SELECTOR = './div[3]/span/a/text()'
                    
                    #information we get from the selector
                    movie_name = movie.css(NAME_SELECTOR).get()
                    movie_name = movie_name[:-4]
                    rating = movie.xpath(RATING_SELECTOR).get()
                    status = movie.xpath(STATUS_SELECTOR).get()
                    genre = movie.xpath(GENRE_SELECTOR).getall()

                    #display the information
                    yield {
                        'movie_name' : movie_name,
                        'rating' : rating,
                        'status' : status,
                        'genre' : genre,
                        }

                #we go to the next page and get that page's information
                NEXT_PAGE_SELECTOR = '.next-page a ::attr(href)'
                next_page = response.css(NEXT_PAGE_SELECTOR).get()
                if next_page:
                        yield scrapy.Request(
                                response.urljoin(next_page),
                                callback=self.parse
                                )
