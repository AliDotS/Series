import requests
from lxml import html
import os
import re

from pymongo import MongoClient

series = MongoClient().imdb.series


movie_exts = r'\.mkv$|\.mp4$|\.avi$|\.flv$|\.mpeg$|\.mpg$'

def getData(name: str):
    if not series.find_one({'name': name}):
        return 0

    url = series.find_one({'name': name})['imdbUrl']

    req = requests.get(url)

    tree = html.fromstring(req.content)

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

    if result.matched_count > 0:
        return 1
    return 0


def createSeries(name: str, url: str, directory: str, urls: [str]):
    if series.find_one({'name': name}):
        return 0

    result = series.insert_one({
        'name': name,
        'imdbUrl': url,
        'directory': directory,
        'urls': urls
    })

    if result.acknowledged:
        return 1

    return 0


def updateSeries(oldName: str, newName: str, url: str, directory: str, urls: [str]):
    result = series.update_one({
        'name': oldName
    }, {
        'name': newName,
        'imdbUrl': url,
        'directory': directory,
        'urls': urls
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

    num = int(
        os.popen(f"find '{tvSeries['directory']}' | grep mkv | grep -Poi \"(?<=e)[0-9][0-9]\" | tail -1").read()) + 1

    episode = '%02i' % num

    season = re.findall("(?<=_)[0-9]+$", tvSeries['imdbUrl'])[0]

    prog = re.compile(f"http[^\ ]*[sS]{season}[^\ ]*[eE]{episode}[^\ ]*mkv")

    for url in tvSeries['urls']:
        page = requests.get(url).content.decode('utf-8')

        results = prog.findall(page)

        # return []
        if results:
            print(results)
            return results
    return


def getSeries():
    for tvSeries in series.find():
        episode = get_last_file(tvSeries['directory'])

        season = re.findall("(?<=_)[0-9]+$", tvSeries['imdbUrl'])[0]

        item = {
            'episode': str(episode),
            'season': season
        }

        item.update(tvSeries)

        yield item

def get_last_file(path):
    biggest = 0
    for _, _, files in os.walk(path):
        for file in files:
            if re.search(movie_exts, file, re.IGNORECASE):
                episode = re.search(r'(?<=[eE])\d{1,2}', file)
                if episode and int(episode.group()) > biggest:
                    biggest = int(episode.group())
    return biggest if biggest > 0 else None

if __name__ == "__main__":
    # print(get_last_file('/media/matrix/ECC6C7AEC6C776FC/Videos/Arrow/Season 07/'))
    getSeries()