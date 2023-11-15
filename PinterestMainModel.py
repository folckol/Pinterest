
import datetime
import ssl
import urllib
from pprint import pprint
import cloudscraper
import requests
import ua_generator

import urllib.parse


csrf = ""
class Account:

    def __init__(self, proxy):

        self.session = self._make_scraper

        self.UA = ua_generator.generate(device="desktop").text
        self.session.proxies = proxy
        self.session.headers.update({"user-agent": self.UA,
                                     "content-type": "application/x-www-form-urlencoded",
                                     "X-Csrftoken": f"{csrf}",
                                     "cookie": f"csrftoken={csrf};"})


        # print(proxy)
        # input()

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def GetRecomendations(self, theme, source_url):

        with self.session.get(
            f"https://ru.pinterest.com/resource/AdvancedTypeaheadResource/get/?source_url={source_url}&data=%7B%22options%22%3A%7B%22pin_scope%22%3A%22pins%22%2C%22count%22%3A5%2C%22term%22%3A%22{theme}%22%7D%2C%22context%22%3A%7B%7D%7D&_={datetime.datetime.now().timestamp()}") as response:
            # pprint(response.json())
            return response.json()['resource_response']['data']['items']
    def GetPhotosFromSearch(self):

        self.pictures = []
        self.picturesLinks = []

        theme = urllib.parse.quote_plus("фото мужчины")

        source_url = urllib.parse.quote_plus(f'/search/pins/?q={theme}&rs=typed')

        recomendations = self.GetRecomendations(theme, source_url)
        for recomendation in recomendations:

            print(recomendation['label'])

            theme_local = urllib.parse.quote_plus(recomendation['label'])
            source_url_local = urllib.parse.quote_plus(f'/search/pins/?q={theme}&rs=typed')

            with self.session.get(f"https://ru.pinterest.com/resource/BaseSearchResource/get/?source_url={source_url_local}&data=%7B%22options%22%3A%7B%22article%22%3Anull%2C%22applied_filters%22%3Anull%2C%22appliedProductFilters%22%3A%22---%22%2C%22auto_correction_disabled%22%3Afalse%2C%22corpus%22%3Anull%2C%22customized_rerank_type%22%3Anull%2C%22filters%22%3Anull%2C%22query%22%3A%22{theme_local}%22%2C%22query_pin_sigs%22%3Anull%2C%22redux_normalize_feed%22%3Atrue%2C%22rs%22%3A%22typed%22%2C%22scope%22%3A%22pins%22%2C%22source_id%22%3Anull%7D%2C%22context%22%3A%7B%7D%7D&_={datetime.datetime.now().timestamp()}") as response:
                # print(response.text)
                # pprint(response.json())
                # input()

                bookmark = response.json()['resource_response']['bookmark']

                data = response.json()['resource_response']['data']['results']
                for i in data:
                    self.pictures.append({'text': i['description'],
                                          'pictures': i['images']})
                    self.picturesLinks.append(i['images']['orig']['url'])

                self.GetPhotosFromBookmark(source_url_local, theme_local, bookmark)

                # for picture in self.pictures:
                #     print(picture['pictures']['orig']['url'])

    def GetPhotosFromBookmark(self,source_url,theme,bookmark):

        with self.session.get(f"https://ru.pinterest.com/resource/BaseSearchResource/get/?source_url={source_url}&data=%7B%22options%22%3A%7B%22article%22%3Anull%2C%22applied_filters%22%3Anull%2C%22appliedProductFilters%22%3A%22---%22%2C%22auto_correction_disabled%22%3Afalse%2C%22corpus%22%3Anull%2C%22customized_rerank_type%22%3Anull%2C%22filters%22%3Anull%2C%22query%22%3A%22{theme}%22%2C%22query_pin_sigs%22%3Anull%2C%22redux_normalize_feed%22%3Atrue%2C%22rs%22%3A%22typed%22%2C%22scope%22%3A%22pins%22%2C%22source_id%22%3Anull%2C%22bookmarks%22%3A%5B%22{bookmark}%22%5D%7D%2C%22context%22%3A%7B%7D%7D") as response:
            # print(response.text)
            # input()
            try:
                bookmark = response.json()['resource_response']['bookmark']
            except:
                pass
            # print(bookmark)
            k = len(self.pictures)
            data = response.json()['resource_response']['data']['results']
            for i in data:

                if i['images']['orig']['url'] not in self.picturesLinks:

                    self.pictures.append({'text': i['description'],
                                          'pictures': i['images']})
                    self.picturesLinks.append(i['images']['orig']['url'])

                    with open('GirlsPhotoResult.txt', 'a+') as file:
                        file.write(i['images']['orig']['url'] + '\n')

            if k == len(self.pictures):
                return True

            print(len(self.pictures))


            # for picture in self.pictures:
            #     pri



            self.GetPhotosFromBookmark(source_url, theme, bookmark)

    @property
    def _make_scraper(self):

        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )

if __name__ == '__main__':

    model = Account(proxy='')

    model.GetPhotosFromSearch()
