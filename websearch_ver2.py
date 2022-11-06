from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import sys, argparse
import re
from urllib.parse import urlparse



# these globals would become class params once this made into a class
site = ""
query = ""
link_depth = int()




def search_wiki(searchterms):
    """
    :param searchterms: The term to search for
    :return: the fully built query string
    """
    searchterms = "_".join(searchterms.split())
    # real search = https://en.wikipedia.org/w/index.php?fulltext=1&search={searchterm}%20&title=Special%3ASearch&ns0=1
    url = f'https://en.wikipedia.org/wiki/{searchterms}_(disambiguation)'

    soup = BeautifulSoup(get_response(url), 'html.parser')
    """
    # for link in soup.find_all("li"):
        # print(link.text)
        # return link.text
    """
    for link in soup.find_all('a', href = re.compile(searchterms)):
            title = link.get('title')
            print(f'{title} : ',link['href'])
            
            follow = link['href']

            print(follow)

            return follow
    


def search_books(searchterms):
    """
    :param searchterms: The term to search for
    :return: the fully built query string
    """
    searchterms = "+".join(searchterms.split())
    url = f'https://www.gutenberg.org/ebooks/search/?submit_search=Go%21&query={searchterms}'

    soup = BeautifulSoup(get_response(url), 'html.parser')

    linklist = []

    depth = int(link_depth)

    # to only ge the link for the book, use[4:9] to ignore the first 4 link, and limit the link to first 5
    for link in soup.findAll(class_='link', href=True)[4:9]:
        
        
        follow = link['href']
        


        linkstr = "https://www.gutenberg.org{}".format(follow)
        linklist.append(linkstr)

    print (linklist)

    return linklist[0:depth]






# main sites to search with query strings
# will have to make this a full dispatch table to custom functions later
sites = {


    "wikipedia": search_wiki,
    "wiki": search_wiki,
    "gutenberg": search_books,
    "books": search_books
}


def init() -> str:
    sysargs = argparse.ArgumentParser(description="Loads passed url to file after initial cleaning (munging).")
    sysargs.add_argument("-s", "--site", help="The site to search (wikipedia, gutenberg)")
    sysargs.add_argument("-q", "--query", help="The term(s) to search for.")
    sysargs.add_argument("-ld", "--link_depth", help="pick to follow how many url from the first 5 url base on the Gutenberg search result ")
    args = sysargs.parse_args()

    # check that all arguments were passed and add site as our global variable
    global site
    global query
    global link_depth


    site = str(args.site).lower()

    try:
        if args.query:
            query = args.query
            link_depth = args.link_depth
            return sites.get(site)(query)
        else:
            print("You must provide both the site (-s,--site) and query string (-q,--q) to use this program.")
            quit(1)
    except (KeyError, TypeError) as ex:
        print("Acceptable sites to search for are: wikipedia(wiki) and gutenberg(books)")
        quit(1)


def get_response(uri):
    # search get and return a response from the url provided

    # Gets website url and provides response
    # If error - exits with exception
    try:
        response = requests.get(uri)
        response.raise_for_status()
    except HTTPError as httperr:
        print(f'HTTP error: {httperr}')
        sys.exit(1)
    except Exception as err:
        print(f"Something went really wrong!: {err}")
        sys.exit(1)

    return response.text


if __name__ == '__main__':

    url = init()


    print(url)

    if site == "books" or site == "gutenberg":
        if url:
            with open(f"{site}_{query}.txt", "w", encoding="utf-8") as f:
                for links in url:
                    f.write(get_response(links))
        else:
            print("First link was un-followable or no links found.")
    else:
        if get_response(url):
            with open(f"{site}_{query}.txt", "w", encoding="utf-8") as f:
                f.write(get_response(url))
        else:
            print("First link was un-followable or no links found.")



    

