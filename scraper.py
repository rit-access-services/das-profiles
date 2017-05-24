import requests
import bs4
from collections import defaultdict


class DasProfileScraper(object):
    BASE_URL = 'http://www.ntid.rit.edu'
    next_url = ''
    staff_directory = None

    def __init__(self, *args, **kwargs):
        if self.next_url == '':
            self.next_url = self.BASE_URL + '/das/directory'
        dd = lambda: defaultdict(dd)  # noqa; E731
        self.staff_directory = dd()

    def set_staff_attr(self, attribute, uids, results):
        for index, item in enumerate(results):
            uid = uids[index]
            uid = self.normalize_uid(uid)
            item = item.get_text()
            self.staff_directory[uid][attribute] = item

    def normalize_uid(self, uid):
        return 'ambdis' if 'Alycia.Morris' in uid else uid

    def scrape(self):
        while self.next_url is not None:
            res = requests.get(self.next_url)
            das_soup = bs4.BeautifulSoup(res.text, 'html.parser')
            next_page_anchor = das_soup.find('a', {'title': 'Go to next page'})
            if next_page_anchor is not None:
                self.next_url = self.BASE_URL + next_page_anchor['href']
            else:
                self.next_url = None

            uids = das_soup.select('span.field-content > a')
            photos = das_soup.select('img.directoryphoto')
            names = das_soup.select('div.views-field-field-lname-value > span > a')
            offices = das_soup.select('div.views-field-field-dasstaff-office-value > span')
            titles = das_soup.select('div.views-field-field-dasstaff-title-value > span')
            phones = das_soup.select('div.views-field-phpcode > span > div.directory_phone')

            for index, uid in enumerate(uids):
                uids[index] = uid.attrs['href'].split('mailto:')[1].split('@')[0]

            for index, photo in enumerate(photos):
                uid = uids[index]
                uid = self.normalize_uid(uid)
                self.staff_directory[uid]['photo'] = photo.attrs['src']

            for index, name in enumerate(names):
                uid = uids[index]
                uid = self.normalize_uid(uid)
                name = name.get_text()
                self.staff_directory[uid]['first_name'] = name.split(' ')[0]
                self.staff_directory[uid]['last_name'] = name.split(' ')[1]

            self.set_staff_attr('office', uids, offices)
            self.set_staff_attr('job_title', uids, titles)

            for index, phone in enumerate(phones):
                uid = uids[index]
                uid = self.normalize_uid(uid)
                phone = phone.get_text()
                phone = ''.join([ch for ch in phone if ch.isdigit()])
                self.staff_directory[uid]['phone'] = phone
        return self.staff_directory
