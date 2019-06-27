import scrapy
import logging
import sys, os
from scrapy.crawler import CrawlerProcess
from os import system,name

#a global variable to store the parsed output
output = {}
genre = []
name = []
page = 0
#a list of menu actions
main_menu_actions = {}
name_menu_actions = {}

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

                    output[movie_name] = [rating, status, genre]
                    #display the information
                    '''
                    yield {
                        'movie_name' : movie_name,
                        'rating' : rating,
                        'status' : status,
                        'genre' : genre,
                        }
                    '''

                #we go to the next page and get that page's information
                NEXT_PAGE_SELECTOR = '.next-page a ::attr(href)'
                next_page = response.css(NEXT_PAGE_SELECTOR).get()
                if next_page:
                        yield scrapy.Request(
                                response.urljoin(next_page),
                                callback=self.parse
                                )
   
###############################
# Menu using the command line
# you can run the menu system
# using "python MeijuScraper.py"
#
###############################                    
def clear():
        if name == 'nt':
                _ = system('cls')
        else:
                _ = system('clear')


def main_menu():
   
    page = 0

    clear()
    print("Welcome to the MeijuScraper. \nThis is a program I created in my free time to \nnavigate my favorite drama site.")
    print("Select the function below to begin\nthe number of drama in the database are now :" , len(output)) 
    print("1. List By Genre")
    print("2. List By Rating")
    print("3. List By Name")
    print("4. Exit")

    choice = input(">>  ")
    exec_menu(choice, "main_menu")
    return

def genre_menu():
    clear()
    print("Listing the movies by genre")
    for i in range(0, len(genre)):
        print(i+1,". ",genre[i])

    print("0. Back")
    choice = input(">>  ")
    exec_menu(choice, "genre_menu")
    return

def rating_menu():
    #TODO sorting algorithm which sort the movies by rating
    clear()
    for movie in output:
        if output[movie][0] != None:
            print(movie,'|',output[movie][0],'|',output[movie][1],'|',output[movie][2])
    return

def name_menu():
    #list all the movies
    clear()
    for i in range(page*10, page*10+10):
        print(name[i])

    print("1. Next")
    print("0. Back")
    choice = input(">>  ")
    exec_menu(choice, "name_menu")
    return

def exit():
    sys.exit()


def exec_menu(choice, fromMenu):
    clear()
    ch = choice.lower()
    if fromMenu == "main_menu":
        if ch == '':
            main_menu_actions['main_menu']()
        else:
            try:
                main_menu_actions[ch]()
            except KeyError:
                print("Invalid selection, please try again. \n")
                main_menu_actions['main_menu']()

    elif fromMenu == "name_menu":
        if ch == '':
            name_menu_actions['name_menu']()
        else:
            try:
                if ch == '1':
                    global page
                    page+=1
                    name_menu_actions[ch]()
                elif ch == '0':
                    name_menu_actions[ch]()
            except Exception as e:
                print(e)
                name_menu_actions['name_menu']()
    return



main_menu_actions = {
    'main_menu': main_menu,
    '1': genre_menu,
    '2': rating_menu,
    '3': name_menu,
    '4': exit,
}
name_menu_actions = {
    'name_menu' : name_menu,
    '1': name_menu,
    '0': main_menu,
}
######################################################
# Several Helper Function (Sorting, Listing, Querying)
######################################################
def unique(list):
    unique_list = []

    for x in list:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def list_genre(data):
    list_of_genre = []
    for movie in data:
        g_genre = data[movie][2]
        for g in g_genre:
            list_of_genre.append(g)
    #we only need unique individual genre
    list_of_genre = unique(list_of_genre)
    return list_of_genre
def list_name(data):
    list_of_name = []
    for movie in data:
        list_of_name.append(movie)
    return list_of_name

if __name__ == "__main__":
        logging.getLogger('scrapy').propagate = False
        process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                })
        process.crawl(MeijuSetSpider)
        print("Please wait for a  few minute for the process to start...\n")
        process.start()
        genre = list_genre(output)
        name = list_name(output)
        main_menu()
        
        
