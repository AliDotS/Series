import requests
from lxml import html
import os
import re
from lxml.html import fromstring
from copy import deepcopy
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime

series = MongoClient().imdb.series


movie_exts = r'\.mkv$|\.mp4$|\.avi$|\.flv$|\.mpeg$|\.mpg$'


def updateAll():
    if not series.find_one():
        return 0

    failed = False
    for tvSeries in getSeries():
        url = tvSeries['imdbUrl']
        content = get_content(url)
        if content is None:
            failed = True
            continue

        tree = html.fromstring(content)
        dates = [e.strip() for e in tree.xpath('//div[@class="airdate"]/text()')]
        names = tree.xpath('//a[@itemprop="name"]/text()')
        result = series.update_one({
            'name': tvSeries['name']
        },
            {
                '$set': {
                    'dates': dates,
                    'names': names,
                }
        })

        if result.matched_count <= 0:
            failed = True

    if failed:
        return False
    return True

def getData(name: str):
    if not series.find_one({'name': name}):
        return False

    url = series.find_one({'name': name})['imdbUrl']

    content = get_content(url)
    if content is None:
        return False
    tree = html.fromstring(content)
    dates = [e.strip() for e in tree.xpath('//div[@class="airdate"]/text()')]
    names = tree.xpath('//a[@itemprop="name"]/text()')
    result = series.update_one({
        'name': name
    },
        {
            '$set': {
                'dates': dates,
                'names': names,
            }
    })

    if result.matched_count <= 0:
        return False
    return True


def createSeries(name: str, url: str, directory: str, urls: [str], photo=''):
    if series.find_one({'name': name}):
        return 0

    if not os.path.isdir(directory):
        return 0

    new_series = {
        'name': name,
        'imdbUrl': url,
        'directory': directory,
        'photo': photo,
        'urls': urls,
        'atStart' : False
    }
    episode = get_last_file(directory)
    if episode is None:
        new_series.update({'atStart': True})
    result = series.insert_one(new_series)

    if result.acknowledged:
        return 1

    return 0


def updateSeries(oldName: str, newName: str, url: str, directory: str, photo: str, urls: [str]):
    result = series.update_one({
        'name': oldName
    }, {
        'name': newName,
        'imdbUrl': url,
        'directory': directory,
        'photo': photo,
        'urls': urls,
        'atStart' : True
    })

    if result.acknowledged:
        return 1

    return 0


def setPhoto(name: str, image: str):
    if not series.find({'name': name}):
        return 0

    result = series.update_one({
        'name': name
    },
        {
            '$set': {
                'image': image
            }
    })

    if result.matched_count > 0:
        return 1
    return 0


def checkOut(name: str):
    if not series.find({'name': name}):
        return -1

    tvSeries = series.find_one({'name': name})

    num = get_last_file(tvSeries['directory'])

    if num is None:
        if tvSeries['atStart']:
            num = 1
        else:
            return
    elif tvSeries['atStart']:
        series.update_one({
            "name" : tvSeries['name']
        },
        {
            '$set': {
                'atStart' : False
            }
        })

    episode = '%02i' % num

    season = re.findall("(?<=_)[0-9]+$", tvSeries['imdbUrl'])[0]

    prog = re.compile(fr"http[^\ ]*[sS]{season}[^\ ]*[eE]{episode}[^\ ]*mkv")

    for url in tvSeries['urls']:
        page = get_content(url)
        if page is None:
            continue
        results = prog.findall(page)

        # return []
        if results:
            print(results)
            return results
    return


def getSeries():
    for tvSeries in series.find():
        episode = get_last_file(tvSeries['directory'])
        if episode is None and tvSeries['atStart']:
            episode = 1

        season = re.findall("(?<=_)[0-9]+$", tvSeries['imdbUrl'])[0]

        item = {
            'episode': str(episode),
            'season': season
        }

        item.update(tvSeries)

        yield item


def getSeriesSingle(name):
    singleSeries = series.find_one({'name': name})

    if not singleSeries:
        return "hello"
    return singleSeries


def get_last_file(path):
    biggest = 0
    for _, _, files in os.walk(path):
        for file in files:
            if re.search(movie_exts, file, re.IGNORECASE):
                episode = re.search(r'(?<=[eE])\d{1,2}', file)
                if episode and int(episode.group()) > biggest:
                    biggest = int(episode.group())
    return biggest if biggest > 0 else None


def get_content(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        return requests.get(url, headers=headers, timeout=20).content.decode('utf-8')
    except Exception:
        return


class imdb_search_result():
    img = ''
    name = ''
    imdb_link = ''

# TODO: url and test not complete


def search(name):
    if not name or name == "":
        return
    site = 'https://www.imdb.com'
    baseUrl = 'https://www.imdb.com/find?s=all&ref_=fn_al_tt_mr&q='
    tree = fromstring(get_content(baseUrl + name))
    # results = tree.xpath('//tr[contains(@class, "findResult")]')
    results = tree.xpath('//*[@id="main"]/div/div[2]/table//tr')
    final_results = []
    details = imdb_search_result()
    for result in results:
        details.img = result.xpath('.//img/@src')[0]
        details.name = result.xpath(
            './/td[@class = "result_text"]/a/text()')[0]
        details.name += result.xpath('.//td[@class = "result_text"]/text()')[1]
        details.imdb_link = result.xpath(
            './/td[@class = "result_text"]/a/@href')[0]
        details.imdb_link = site + details.imdb_link
        final_results.append(deepcopy(details))
    return final_results if final_results else None


def get_season(imdb_id: str):
    url = f"https://www.imdb.com/title/{imdb_id}/episodes?season=1"
    content = get_content(url)
    if not content:
        return
    tree =  fromstring(content)
    season = tree.xpath('//*[@id="bySeason"]/option[last()]/text()')
    try:
        season = int(season[0].strip())
    except Exception:
        return
    # return get_confirmed_season(imdb_id, season)




def get_dates(imdb_id, season):
    url = f"https://www.imdb.com/title/{imdb_id}/episodes?season={season}"
    content = get_content(url)
    if not content:
        return
    tree =  fromstring(content)
    return [e.strip() for e in tree.xpath('//div[@class="airdate"]/text()')]


if __name__ == "__main__":
    # print(get_last_file('/media/matrix/ECC6C7AEC6C776FC/Videos/Arrow/Season 07/'))
    # pprint(search('robocop')[0].__dict__)
    # pprint(getSeriesSingle('bigbang'))
    print(get_season('tt4158110'),\
        get_season('tt6468322'))
