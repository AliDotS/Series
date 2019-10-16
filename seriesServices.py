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
        imdbId = tvSeries['imdbId']
        season = tvSeries['season']
        url = f"https://www.imdb.com/title/{imdbId}/episodes?season={season}"
        content = get_content(url)
        if content is None:
            failed = True
            continue

        tree = html.fromstring(content)
        dates = [e.strip() for e in tree.xpath(
            '//div[@class="airdate"]/text()')]
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
    tvSeries = series.find_one({'name': name})
    if not tvSeries:
        return False
    imdbId = tvSeries['imdbId']
    season = tvSeries['season']
    url = f"https://www.imdb.com/title/{imdbId}/episodes?season={season}"

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


def createSeries(name: str, imdbId: str, season: int, directory: str, urls: [str], photo=''):
    if series.find_one({'name': name}):
        return 0

    if not os.path.isdir(directory):
        return 0

    new_series = {
        'name': name,
        'imdbId': imdbId,
        'season': season,
        'directory': directory,
        'photo': photo,
        'urls': urls,
        'atStart': False
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
        '$set': {
            'name': newName,
            'imdbUrl': url,
            'directory': directory,
            'photo': photo,
            'urls': urls,
            'atStart': True
        }
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
                'photo': image
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
            "name": tvSeries['name']
        },
            {
            '$set': {
                'atStart': False
            }
        })

    episode = '%02i' % num

    season = tvSeries['season']

    prog = re.compile(
        fr"http[^\ ]*[sS]{season:02}[^\ ]*[eE]{episode}[^\ ]*mkv")

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

        season = tvSeries['season']

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
    imdb_id = ''

# TODO: url and test not complete


def search(name):
    if not name or name == "":
        return
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
        details.imdb_id = result.xpath(
            './/td[@class = "result_text"]/a/@href')[0]
        details.imdb_id = re.search(
            r'(?<=title/)tt\d+(?=/)', details.imdb_id).group()
        final_results.append(deepcopy(details))
    return final_results if final_results else None


def get_season(imdb_id: str):
    url = f"https://www.imdb.com/title/{imdb_id}/episodes?season=1"
    content = get_content(url)
    if not content:
        return
    tree = fromstring(content)
    season = tree.xpath('//*[@id="bySeason"]/option[last()]/text()')
    try:
        season = int(season[0].strip())
    except Exception:
        return
    return get_confirmed_season(imdb_id, season)


def get_confirmed_season(imdb_id, season):
    dates = {}
    dates.update({season: get_dates(imdb_id, season)})
    now = datetime.now()
    while(season > 0):
        for index, date in reversed(list(enumerate(dates[season]))):
            try:
                if '.' in date:
                    current = datetime.strptime(date, "%d %b. %Y").date()
                else:
                    current = datetime.strptime(date, "%d %b %Y").date()
            except Exception:
                continue
            if current <= now.date():
                if index == len(dates[season]) - 1:
                    return season + 1
                else:
                    return season
        season -= 1
        dates.update({season: get_dates(imdb_id, season)})


def get_dates(imdb_id, season):
    url = f"https://www.imdb.com/title/{imdb_id}/episodes?season={season}"
    content = get_content(url)
    if not content:
        return
    tree = fromstring(content)
    return [e.strip() for e in tree.xpath('//div[@class="airdate"]/text()')]


def check_date(name: str):
    tvSeries = series.find_one({'name': name})
    if not tvSeries or not tvSeries.get('dates'):
        return
    now = datetime.now().date()
    episode = get_last_file(tvSeries['directory'])
    if episode is None:
        return
    date = tvSeries['dates'][episode - 1]
    try:
        if '.' in date:
            date = datetime.strptime(date, '%d %b. %y').date()
        else:
            date = datetime.strptime(date, '%d %b %Y').date()
    except Exception:
        return
    return (now - date).days



if __name__ == "__main__":
    # print(get_last_file('/media/matrix/ECC6C7AEC6C776FC/Videos/Arrow/Season 07/'))
    # pprint(search('robocop')[0].__dict__)
    # pprint(getSeriesSingle('bigbang'))
    # print(get_season('tt4158110'),\
    #     get_season('tt6468322'))
    print(check_date('bigbang'))