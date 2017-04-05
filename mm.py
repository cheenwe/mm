# encoding=utf-8

import re
import os
import utils
import urllib2
from sqlhelper import SqlHelper
from bs4 import BeautifulSoup as bs

class Crawler(object):
    def __init__(self):
        super(Crawler, self).__init__()
        self.album_prefix = 'https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20={0}&page={1}'
        self.image_prefix = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id={0}&album_id={1}&page={2}'
        self.image_pattern = re.compile('''img.*290x10000.jpg''', re.U)
        self.image_name_pattern = re.compile('''"picId":"(.*?)"''', re.U)
        self.model_pattern = re.compile('''<a class="lady-name" href="(.*?)".*>(.*?)</a>''', re.U)
        self.album_pattern = re.compile('''.*album_id=(.*?)&.*''', re.U)
        self.links = []
        self.ids= []
        self.names= []
        self.sql = SqlHelper()


    def readHtml(self, html):
        response = urllib2.urlopen(html)
        return response.read()

    def getLinkIdAndNames(self, htmlData):
        items = re.findall(self.model_pattern, htmlData)
        self.links = [link for link, name in items]
        self.names = [name.decode('gbk') for link, name in items]
        self.ids = [link[link.index('=')+1:] for link in self.links]

    def getAlbums(self):
        for i, model_id in enumerate(self.ids):

            utils.log('start downloading:%s' % self.names[i])
            # print 'start downloading', self.names[i]

            # 插入用户
            command = self.sql.insert_data_to_users()
            msg = (model_id, self.names[i], "",)

            try:
                self.sql.insert_data(command, msg, commit = True)
            except Exception, e:
                utils.log('insert users data errors')


            for page in xrange(1, 10):
                utils.log('current page:%s' % page)
                # print 'current page', page

                model_url = self.album_prefix.format(model_id, page)
                soup = bs(self.readHtml(model_url), 'html.parser')
                albums = soup.find_all('div', class_ = 'mm-photo-cell-middle')
                if not albums:
                    break
                for album in albums:
                    album_name = album.find('h4').a.string.strip().rstrip('.')
                    album_link= album.find('h4').a['href']
                    album_id = re.findall(self.album_pattern, album_link)[0]
                    album_create_time = album.find('p', class_ = 'mm-photo-date').string.strip(u'创建时间: ').strip(u'´´½¨Ê±¼ä:')
                    album_img_count = album.find('span', class_ = 'mm-pic-number').string.strip('()').strip(u'张').strip(u'ÕÅ')

                    # print ">>>>>>>>>>>>>>>>>>>>>>"
                    # print album.find('p', class_ = 'mm-photo-date').string
                    # print album_create_time
                    # print ">>>>>>>>>>>>>>>>>>>>>>"

                    # 插入相册
                    command = self.sql.insert_data_to_albums()
                    msg = (album_id, model_id, album_name, album_create_time, "", 1, album_img_count)
                    try:
                        self.sql.insert_data(command, msg, commit = True)
                    except Exception, e:
                        utils.log('insert albums data errors')


                    utils.log('start in album:%s, total size: %s' % (album_name, album_img_count))

                    self.getImages(model_id, album_id, album_img_count)


    def getImages(self, model_id, album_id, image_count):
        # print 'start downloading album', album_id, image_count, '张'
        for page in xrange(1, (int(image_count)-1)/16+2):
            link = self.image_prefix.format(model_id, album_id, page)
            body = self.readHtml(link).decode('gbk')
            images = re.findall(self.image_pattern, body)
            # tried to use des as names, however, it duplicates times. So i chose pic ids.
            names = re.findall(self.image_name_pattern, body)
            for idx, image in enumerate(images):
                image = image.replace('290', '620')
                try:
                    img_url = ('http://'+image).replace('jpg_620x10000.jpg','jpg')
                except Exception as e:
                    img_url = ('http://'+image)

                # id , album_id , name  , url , kind

                # 插入图片
                command = self.sql.insert_data_to_photos()
                msg = (None, album_id, "", img_url,  1)
                try:
                    self.sql.insert_data(command, msg, commit = True)
                except Exception, e:
                    utils.log('insert photos data errors')


                # print 'created photos success'


if __name__ == '__main__':
    test_html = 'https://mm.taobao.com/json/request_top_list.htm?page={0}'
    for page in xrange(1, 100):
        c = Crawler()
        data = c.readHtml(test_html.format(page))
        c.getLinkIdAndNames(data)
        c.getAlbums()
