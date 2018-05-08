import urllib.request
from datetime import datetime

from module import base
from module import short_url
from bs4 import BeautifulSoup

from module import tele_api


class gnuNotification(base.baseNotifier):
    def __init__(self):
        super().__init__()

        self.mode = 'GNU'
        self.load_id()

    def run(self):
        url = 'http://www.gnu.ac.kr/program/multipleboard/BoardView.jsp?groupNo=10026&boardNo=' + str(self.id)
        try:
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, 'html5lib')
            # title_list = soup.select_one('.title) # selector option (testing)
            title_list = soup.find_all('h3')
        except:
            print('GNU_NOTI: ERROR OCCURED during scraping', datetime.now())
            return

        html.close()
        noti_title = self.parse_title(title_list, findAllIndex=3)  # at HOT NEWS, Index is 3.

        if noti_title == False:
            print('GNU_NOTI: There is no notification. ID:', self.id, datetime.now())
            self.check()

        else:
            noti_title = '[HOT NEWS]\n' + noti_title
            short = short_url.makeShort(url)
            tele = tele_api.Telegram('@Testing77') #Should Edit at live server
            tele.notification(noti_title, short)
            print('GNU_NOTI: NEW NOTIFICATION. ID:', self.id)
            self.id += 1
            self.save_id()

    def save_id(self):
        path = self.root + '\source\last_gnu'
        super().save(self.id, path)

    def load_id(self):
        path = self.root + '\source\last_gnu'
        self.id = super().load(path)