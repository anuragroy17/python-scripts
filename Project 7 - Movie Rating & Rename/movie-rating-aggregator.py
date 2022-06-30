import os
import re
import urllib.request
import unicodedata
from imdb import Cinemagoer, IMDbError


def folders():
    DIRECTORY = 1
    return next(os.walk(os.curdir))[DIRECTORY]


def strip_quality(path):
    path, brcount = re.subn('brrip$', '', path, count=0, flags=re.IGNORECASE)
    path, dvdcount = re.subn('dvdrip$', '', path, count=0, flags=re.IGNORECASE)
    rip = ''
    if brcount == 1:
        rip = ' BRRip'
    elif dvdcount == 1:
        rip = ' DVDRip'

    return path, rip


def get_name_from_folder(path):
    path = re.sub('^[12][0-9]{3}', '', path)
    path = path.rstrip(') ')
    path = re.sub('[12][0-9]{3}$', '', path)
    path = path.strip('() ')
    return path


def get_year_from_folder(path):
    x = re.search('.*([1-3][0-9]{3})', path)
    year = None
    if bool(x):
        year = x.group(1)
    return bool(x), year


def imdb_url(path):
    url = 'http://www.imdb.com/find?q=' + '+'.join(path.split(' '))
    url = unicodedata.normalize('NFKD', url).encode(
        'ascii', errors='ignore').decode('ascii')
    return url


def crawl_imdb(url):
    request = urllib.request.Request(
        url, None, {'Accept-Language': 'en-US,en;q=0.8,de;q=0.6'})
    response = urllib.request.urlopen(request)
    content = response.read()
    text = content.decode('utf-8-sig', errors='ignore')
    return text


def get_rating(title, movie_year):
    try:
        ia = Cinemagoer()

        movie_search = ia.search_movie(title)
        movie_id, title_from_imdbPy = get_movie_id(
            movie_search, movie_year)
        if movie_id == None:
            return movie_id, title_from_imdbPy

        movie = ia.get_movie(movie_id, info=['vote details'])
        # print('median', movie.get('median'))
        # print('arithmetic mean', movie.get('arithmetic mean'))
        # print('number of votes', movie.get('number of votes'))
        return movie.get('demographics').get('ttrt fltr imdb users').get('rating'), title_from_imdbPy
    except IMDbError as e:
        # print(e)
        return None, None


def get_movie_id(movie_search, movie_year):
    for i in range(len(movie_search)):
        if str(movie_search[i]['year']) == str(movie_year) and movie_search[i]['kind'] == 'movie':
            return movie_search[i].movieID, movie_search[i]['title']
    return None, None


def parse_title(html):
    matches = re.search('"result_text">[^>]+>(?P<title>[^<]*)', html)
    if not matches:
        return None
    title = matches.group('title')
    title = title.strip()
    if len(title) > 3 and re.match('[0-9A-Za-z-,!?]+', title):
        return title
    return None


def parse_year(html):
    matches = re.search('"result_text">[^>]+>[^>]+> (?P<text>[^<]+) <', html)
    if not matches:
        return None
    text = matches.group('text')
    matches = re.search('(?P<year>[12][0-9]{3})', text)
    if matches:
        return matches.group('year')
    return None


def fetch_movie(name):
    url = imdb_url(name)
    html = crawl_imdb(url)
    title = parse_title(html)
    year = parse_year(html)
    return title, year


def get_movie_details(extracted_name, year_present, year_from_folder):
    fetched_rating = None
    if year_present:
        # print('fetching from imdbpy...')
        title = extracted_name
        year = str(year_from_folder)
        fetched_rating, title = get_rating(title, year)

    if fetched_rating == None:
        # print('fetching from imdb url...')
        title, year = fetch_movie(extracted_name)
        fetched_rating, title_from_imdbpy = get_rating(title, year)

    rating = 'R-' + str(fetched_rating)
    return title, year, rating


def remove_subtitle(title):
    title = strip_after(title, '-')
    title = strip_after(title, ':')
    title = title.rstrip(' ')
    return title


def strip_after(string, character):
    position = string.rfind(character)
    if position > 0:
        string = string[:position]
    return string


def replace_colon(title):
    return title.replace(":", "-")


def compare_titles(local, fetched):
    local = strip_after(local, '-')
    local = strip_after(local, ':')
    fetched = strip_after(fetched, '-')
    fetched = strip_after(fetched, ':')
    ignore = '[-.,()\'" ]+'
    local = re.sub(ignore, '', local).lower()
    fetched = re.sub(ignore, '', fetched).lower()
    return local == fetched


def user_decision(name, title):
    letter = None
    while not (letter == 'n' or letter == 'y'):
        letter = input('> Rename \'' + name +
                       '\' to \'' + title + '\'? (y/n) ')
    return letter == 'y'


def rename(path_from, path_to):
    absolute_from = os.path.join(os.getcwd(), path_from)
    absolute_to = os.path.join(os.getcwd(), path_to)
    try:
        os.rename(absolute_from, absolute_to)
        return True
    except:
        return False


def print_line(folder, year, title, rename_to, action):
    def format(string, length=35):
        if len(string) > length:
            return string[:length-3] + '...'
        else:
            return string.ljust(length)
    print(format(folder), year.ljust(4), format(
        title), format(rename_to), action, flush=True)


def print_change(folder, year, title, output, action):
    print_line(folder, year, title, output, action)


#not used
def has_year(path):
    left = re.compile('^[1-2][0-9]{3}')
    right = re.compile('[1-2][0-9]{3}$')
    path = re.sub('[()]', '', path)
    path = path.strip()
    return left.match(path) or right.match(path)


##### START ######
print_line('Input folder', 'Year', 'Title', 'Output folder', 'Action')
print('-' * (37 * 3 + 14))

for folder in folders():
    raw_name, rip = strip_quality(folder)

    if bool(re.search('R-[0-9]', raw_name)):
        title = ''
        year = ''
        action = 'Already Rated'
        print_change(folder, '', '', '', action)
        continue

    extracted_name = get_name_from_folder(raw_name)
    year_present, year_from_folder = get_year_from_folder(raw_name)

    title, year, rating = get_movie_details(
        extracted_name, year_present, year_from_folder)

    rename_to = ''
    action = 'Error'
    if title and year:
        # title = remove_subtitle(title)
        title = replace_colon(title)
        rename_to = title + ' (' + year + ') ' + rating + rip
        if folder == rename_to:
            action = 'Equal'
        elif compare_titles(extracted_name, title):
            if rename(folder, rename_to):
                action = 'Renamed'
            else:
                action = 'Error'
        elif user_decision(extracted_name, title):
            if rename(folder, rename_to):
                action = 'Renamed'
            else:
                action = 'Error'
        else:
            action = 'Discarded'
    else:
        title = ''
        year = ''
        action = 'Not found'
    print_change(folder, year, title, rename_to, action)

print('')
os.system('pause')


# ToDo
# 1) Use any directory (take input from user)
# 2) fetch rating from imdb url
