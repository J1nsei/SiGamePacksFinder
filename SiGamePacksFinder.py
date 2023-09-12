import csv
import requests
import argparse
import time
from datetime import date
from tqdm import tqdm

class SiGameParser:

    def __init__(self, token: str = 'undefined', min_likes: int = 6):
        self.token = token
        self.min_likes = min_likes
        self.version = 5.131
        self.group_id = 135725718
        self.topic_id = 34975471
        self.like = True
        self.offset = 0
        self.count = 100
        self.max_requests = 5
        self.check_token()
        self.max_offset = self.get_max_offset()
        self.parsed_data = []

    def make_response(self):
        response = requests.get('https://api.vk.com/method/board.getComments',
                                params={
                                   'access_token': self.token,
                                   'v': self.version,
                                   'group_id': self.group_id,
                                   'topic_id': self.topic_id,
                                   'need_likes': self.like,
                                   'count': self.count,
                                   'offset': self.offset
                                })
        return response.json()

    def check_token(self):
        response = self.make_response()
        if 'error' in response.keys():
            raise Exception('Wrong token')

    def get_max_offset(self):
        response = self.make_response()
        max_offset = response['response']['count']
        return max_offset

    def parse(self):
        response_count = 0
        pbar = tqdm(total=self.max_offset, desc='Search for packages')
        while self.offset < self.max_offset:
            response = self.make_response()
            self.parsed_data.extend(response['response']['items'])
            self.offset += self.count
            response_count += 1
            if response_count > self.max_requests:
                time.sleep(1)
                response_count = 0
            pbar.update(self.count)

    def save(self):
        with open('SiGamePackages.csv', 'w', encoding='cp1251', errors='ignore') as file:
            a_open = csv.writer(file, delimiter=';')
            a_open.writerow(('  Лайки', 'Описание', ' Ссылка', '№ поста', '  Дата'))
            for post in self.parsed_data:
                if 'attachments' in post and post['likes']['count'] >= self.min_likes:
                    for att in post['attachments']:
                        if att['type'] == 'doc' and att['doc']['ext'] == 'siq':
                            post_likes = post['likes']['count']
                            post_text = post['text']
                            post_id = str(post['id'])
                            post_date = ' ' + date.fromtimestamp(att['doc']['date']).strftime('%Y-%m-%d')
                            post_link = '=ГИПЕРССЫЛКА("https://vk.com/topic-135725718_34975471?post=' \
                                        + post_id + '";"Открыть")'
                            a_open.writerow((post_likes, post_text, post_link, post_id, post_date))
                            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_likes', '--ml', default=6, type=int,
                        help='Minimum number of likes on a post containing packages')
    args = parser.parse_args()
    min_likes = args.min_likes
    with open('token.txt', 'r') as token_file:
        token = token_file.read().strip()
    FindPacks = SiGameParser(token, min_likes)
    FindPacks.parse()
    FindPacks.save()
