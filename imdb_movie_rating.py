import sys
import json
#import httplib2
import urllib2
from HTMLParser import HTMLParser
import copy

SEARCH_REQUEST_URL = str('https://www.imdb.com/search/title?title={movie_name}&title_type=feature')
GET_MOVIE_URL = str('https://www.imdb.com/title/{imdb_title_id}/ratings?ref_=tt_ov_rt')

class MyHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.movie_title = {} 
        self.prev = None
        self.rating = None
        self.found_ratings_imdb_rating = False

    def handle_starttag(self, tag, attrs):
        temp = []
        for k,v in attrs:
            if v != None and v.strip().endswith('ratings-imdb-rating'):
                self.found_ratings_imdb_rating = True
            if not self.rating and self.found_ratings_imdb_rating:
                if k == 'data-value':
                    self.rating = v
                    #print v

            if k == 'href':
                self.prev = v
            elif str(k.strip()) == 'alt':
                try:
                    key = v.lower().replace(' ','_')
                    value = self.prev.split('/')[2]
                    self.movie_title[ key.lower() ] = value
                    #print key , ' : ' , value

                except:
                    pass
            elif k == 'title':
                pass
                #print v

    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        pass

    def handle_data(self, data):
        #print "Encountered some data  :", data
        #print data
        pass



def get_url_content( url , replace_key, replace_value):
    
    movie_url = str(url).replace(replace_key, replace_value)
    #print movie_url
    
    req = urllib2.Request(movie_url)
    
    response=urllib2.urlopen(req)
    
    parser = MyHTMLParser()
    for i in response:
        #if url == GET_MOVIE_URL:
        #    print i
        parser.feed(i)
    parser.close()
    
    return parser



if __name__ == '__main__':
    #global movie_title
    if len(sys.argv) == 2:
        movie_name = sys.argv[1]
        #print movie_name
        p = get_url_content(SEARCH_REQUEST_URL, '{movie_name}' , movie_name.replace(' ','+'))
        key = str(movie_name.strip().lower()).replace(' ','_')
        #print 'movie stripped : ' , key 
        imdb_title_id = None
        for k in p.movie_title.keys():
            #print k.strip().lower()
            if k.strip().lower() == key:
                imdb_title_id = p.movie_title[ key ]
                #print imdb_title_id

        if imdb_title_id == None:
            print 'Could not find movie ' , movie_name
            sys.exit(1) 

        movie = get_url_content(GET_MOVIE_URL, '{imdb_title_id}' , imdb_title_id )

        print movie_name , 'rating is' , movie.rating

