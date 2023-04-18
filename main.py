import csv

import requests

from model import Items


class PetrovichParser:
    def __init__(self, category: str):
        self.category = category
        self.url = self.get_url()

    def get_url(self):
        items_dict = {
            'электроинструмент': '18978',
            'ручной инструмент': '9799',
            'расходные материалы к электроинструменту': '18970',
            'абразивные материалы': '10477',
            'высотные конструкции': '18736',
            'расходные материалы, хозтовары': '10536',
            'спецодежда и средства защиты': '1407',
            'бензоинструмент и принадлежности': '18980',
            'газовое и сварочное оборудование': '4102',
            'измерительные инструменты': '19003',
            'силовая, строительная техника и комплектующие': '18932',
        }
        if category_num := items_dict.get(self.category):
            return f'https://api.petrovich.ru/catalog/v3/sections/{category_num}/products'
        raise Exception("Я не знаю такой категории")

    @property
    def cookies(self):
        cookies = {
            'SNK': '119',
            'u__typeDevice': 'desktop',
            'SIK': 'dwAAAJbOmnrwuVMTvBgMAA',
            'SIV': '1',
            'C_eEWCwtew6_o2LI1CfCprIKXEo54': 'AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAAD-eunpQUqJlfOGTXyWebwAR62CkXQ',
            'ssaid': 'd9c52270-d897-11ed-ad1b-71171f3ce653',
            '_ym_uid': '1681238223170695693',
            '_ym_d': '1681238223',
            'tmr_lvid': '959ac31755fc9c234e66b436aca785ca',
            'tmr_lvidTS': '1681238222674',
            'rrpvid': '954823828563217',
            'FPID': 'FPID2.2.lqn4lsIOZlOMsEOZ6HTe1QisSYYA1yVvNmq05p%2Fucbo%3D.1681238222',
            'rcuid': '6329ee0be15ca071ce4d69b1',
            'count_buy': '0',
            'js_FPID': 'FPID2.2.lqn4lsIOZlOMsEOZ6HTe1QisSYYA1yVvNmq05p%2Fucbo%3D.1681238222',
            'js_SIK': 'dwAAAJbOmnrwuVMTvBgMAA',
            'ser_ym_uid': '1681238223170695693',
            'UIN': 'dwAAADOu1hFpqHwxWI9XR3v8FGtoasNb9LlTExBsCgA',
            'js_count_buy': '0',
            'u__geoCityGuid': 'b835705e-037e-11e4-9b63-00259038e9f2',
            'u__geoUserChoose': '1',
            'dd_user.isReturning': 'true',
            'dd_custom.lt15': '2023-04-12T16:32:09.434Z',
            'dd_custom.ts16': '{%22ttl%22:2592000%2C%22granularity%22:86400%2C%22data%22:{%221681257600%22:4}}',
            'dd_custom.lastViewedProductImages': '[%221214420%22%2C%2218363%22%2C%2238992%22]',
            'dd_custom.ts12': '{%22ttl%22:2592000%2C%22granularity%22:86400%2C%22data%22:{%221681171200%22:1%2C%221681257600%22:1%2C%221681344000%22:2%2C%221681430400%22:3}}',
            'dd_custom.lt11': '2023-04-14T15:25:34.570Z',
            'rrlevt': '1681485935341',
            'dd__persistedKeys': '[%22custom.lastViewedProductImages%22%2C%22custom.lt13%22%2C%22custom.ts14%22%2C%22custom.ts12%22%2C%22custom.lt11%22%2C%22user.isReturning%22%2C%22custom.lt15%22%2C%22custom.ts16%22]',
            '_gid': 'GA1.2.1507712572.1681741167',
            'FPLC': 'h7AF7zH8Q9KAzUVLgQ7VhEclKdTw7wuB80VzqmQac4ZSHbU5O%2BpInLlUKLLAozbGgF7ktllsBvKk5CHwiI3fjJHrxF6i%2BCY2kLSiiP6HzHlQuGN1FSlwl31nTTx%2BGg%3D%3D',
            '_ym_isad': '1',
            '_ym_visorc': 'b',
            'dd_custom.lt13': '2023-04-18T18:21:52.414Z',
            'dd_custom.ts14': '{%22ttl%22:2592000%2C%22granularity%22:86400%2C%22data%22:{%221681171200%22:7%2C%221681257600%22:5%2C%221681344000%22:16%2C%221681430400%22:10%2C%221681516800%22:1%2C%221681603200%22:1%2C%221681689600%22:3%2C%221681776000%22:5}}',
            'digi_uc': 'W1sidiIsIjEwNDQ5OCIsMTY4MTQ4NTkzNDUxM10sWyJ2IiwiMTA1Njc5IiwxNjgxNDg1ODc4NTE2XSxbInYiLCIxMzM1NTYiLDE2ODE0ODU3NzkzMzRdLFsidiIsIjYzNjI3NSIsMTY4MTM4OTg4Mzg3MF0sWyJ2IiwiMTYyMzY1IiwxNjgxMzE4OTQwMDAxXSxbInYiLCI5ODc1NjgiLDE2ODEyMzg5OTI4OTddLFsiY3YiLCIxMDU2NzkiLDE2ODE4NDIxMTExMzhdLFsiY3YiLCI4Mjg2NTQiLDE2ODE4NDE4NDUyMDJdLFsiY3YiLCI2OTE3ODEiLDE2ODE4MDMxODExNzBdLFsiY3YiLCIxMDQ0OTgiLDE2ODE0ODYwODk3NzZdLFsiY3YiLCIxMDkyMzAiLDE2ODE0ODU3NzMzNDVdLFsiY3YiLCI4MTM3OTkiLDE2ODE0MTQxMzY3NjhdLFsiY3YiLCI2Njc4MjEiLDE2ODE0MDQ2ODM0MjBdLFsiY3YiLCI3OTc4MzciLDE2ODEzOTkyMzM0MTJdLFsiY3YiLCIxNjIzNjUiLDE2ODEzODk4ODU1NDBdLFsiY3YiLCI2ODk3NzUiLDE2ODEzODk4NzM0MTldLFsic3YiLCIxNjIzNjUiLDE2ODEzMTcxMjg1OTVdXQ==',
            'mindboxDeviceUUID': 'a7fd15f4-7f09-4567-8b16-7096c01bba4f',
            'directCrm-session': '%7B%22deviceGuid%22%3A%22a7fd15f4-7f09-4567-8b16-7096c01bba4f%22%7D',
            '_ga_XW7S332S1N': 'GS1.1.1681841844.28.1.1681842189.57.0.0',
            '_dc_gtm_UA-23479690-1': '1',
            '_ga': 'GA1.2.1237826282.1681238222',
            '_dc_gtm_UA-23479690-19': '1',
            '__tld__': 'null',
            'dd__lastEventTimestamp': '1681842194412',
        }
        return cookies

    @property
    def headers(self):
        headers = {
            'authority': 'api.petrovich.ru',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,fi;q=0.6,nb;q=0.5,is;q=0.4,pt;q=0.3,ro;q=0.2,it;q=0.1,de;q=0.1',
            # 'cookie': 'SNK=119; u__typeDevice=desktop; SIK=dwAAAJbOmnrwuVMTvBgMAA; SIV=1; C_eEWCwtew6_o2LI1CfCprIKXEo54=AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAAD-eunpQUqJlfOGTXyWebwAR62CkXQ; ssaid=d9c52270-d897-11ed-ad1b-71171f3ce653; _ym_uid=1681238223170695693; _ym_d=1681238223; tmr_lvid=959ac31755fc9c234e66b436aca785ca; tmr_lvidTS=1681238222674; rrpvid=954823828563217; FPID=FPID2.2.lqn4lsIOZlOMsEOZ6HTe1QisSYYA1yVvNmq05p%2Fucbo%3D.1681238222; rcuid=6329ee0be15ca071ce4d69b1; count_buy=0; js_FPID=FPID2.2.lqn4lsIOZlOMsEOZ6HTe1QisSYYA1yVvNmq05p%2Fucbo%3D.1681238222; js_SIK=dwAAAJbOmnrwuVMTvBgMAA; ser_ym_uid=1681238223170695693; UIN=dwAAADOu1hFpqHwxWI9XR3v8FGtoasNb9LlTExBsCgA; js_count_buy=0; u__geoCityGuid=b835705e-037e-11e4-9b63-00259038e9f2; u__geoUserChoose=1; dd_user.isReturning=true; dd_custom.lt15=2023-04-12T16:32:09.434Z; dd_custom.ts16={%22ttl%22:2592000%2C%22granularity%22:86400%2C%22data%22:{%221681257600%22:4}}; dd_custom.lastViewedProductImages=[%221214420%22%2C%2218363%22%2C%2238992%22]; dd_custom.ts12={%22ttl%22:2592000%2C%22granularity%22:86400%2C%22data%22:{%221681171200%22:1%2C%221681257600%22:1%2C%221681344000%22:2%2C%221681430400%22:3}}; dd_custom.lt11=2023-04-14T15:25:34.570Z; rrlevt=1681485935341; dd__persistedKeys=[%22custom.lastViewedProductImages%22%2C%22custom.lt13%22%2C%22custom.ts14%22%2C%22custom.ts12%22%2C%22custom.lt11%22%2C%22user.isReturning%22%2C%22custom.lt15%22%2C%22custom.ts16%22]; _gid=GA1.2.1507712572.1681741167; FPLC=h7AF7zH8Q9KAzUVLgQ7VhEclKdTw7wuB80VzqmQac4ZSHbU5O%2BpInLlUKLLAozbGgF7ktllsBvKk5CHwiI3fjJHrxF6i%2BCY2kLSiiP6HzHlQuGN1FSlwl31nTTx%2BGg%3D%3D; _ym_isad=1; _ym_visorc=b; dd_custom.lt13=2023-04-18T18:21:52.414Z; dd_custom.ts14={%22ttl%22:2592000%2C%22granularity%22:86400%2C%22data%22:{%221681171200%22:7%2C%221681257600%22:5%2C%221681344000%22:16%2C%221681430400%22:10%2C%221681516800%22:1%2C%221681603200%22:1%2C%221681689600%22:3%2C%221681776000%22:5}}; digi_uc=W1sidiIsIjEwNDQ5OCIsMTY4MTQ4NTkzNDUxM10sWyJ2IiwiMTA1Njc5IiwxNjgxNDg1ODc4NTE2XSxbInYiLCIxMzM1NTYiLDE2ODE0ODU3NzkzMzRdLFsidiIsIjYzNjI3NSIsMTY4MTM4OTg4Mzg3MF0sWyJ2IiwiMTYyMzY1IiwxNjgxMzE4OTQwMDAxXSxbInYiLCI5ODc1NjgiLDE2ODEyMzg5OTI4OTddLFsiY3YiLCIxMDU2NzkiLDE2ODE4NDIxMTExMzhdLFsiY3YiLCI4Mjg2NTQiLDE2ODE4NDE4NDUyMDJdLFsiY3YiLCI2OTE3ODEiLDE2ODE4MDMxODExNzBdLFsiY3YiLCIxMDQ0OTgiLDE2ODE0ODYwODk3NzZdLFsiY3YiLCIxMDkyMzAiLDE2ODE0ODU3NzMzNDVdLFsiY3YiLCI4MTM3OTkiLDE2ODE0MTQxMzY3NjhdLFsiY3YiLCI2Njc4MjEiLDE2ODE0MDQ2ODM0MjBdLFsiY3YiLCI3OTc4MzciLDE2ODEzOTkyMzM0MTJdLFsiY3YiLCIxNjIzNjUiLDE2ODEzODk4ODU1NDBdLFsiY3YiLCI2ODk3NzUiLDE2ODEzODk4NzM0MTldLFsic3YiLCIxNjIzNjUiLDE2ODEzMTcxMjg1OTVdXQ==; mindboxDeviceUUID=a7fd15f4-7f09-4567-8b16-7096c01bba4f; directCrm-session=%7B%22deviceGuid%22%3A%22a7fd15f4-7f09-4567-8b16-7096c01bba4f%22%7D; _ga_XW7S332S1N=GS1.1.1681841844.28.1.1681842189.57.0.0; _dc_gtm_UA-23479690-1=1; _ga=GA1.2.1237826282.1681238222; _dc_gtm_UA-23479690-19=1; __tld__=null; dd__lastEventTimestamp=1681842194412',
            'origin': 'https://moscow.petrovich.ru',
            'referer': 'https://moscow.petrovich.ru/catalog/18978/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
        return headers

    def params(self, offset: int):
        params = {
            'limit': '50',
            'offset': offset,
            # 'path': '/catalog/18978/',
            'city_code': 'msk',
            'client_id': 'pet_site',
        }
        return params

    def save_csv(self, items):
        with open(f"{self.category}.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.code, product.title, product.price.gold])

    def parse(self):
        offset = 0
        while True:
            response = requests.get(
                self.url,
                params=self.params(offset=offset),
                cookies=self.cookies,
                headers=self.headers,
            )
            if response.status_code != 200:
                break
            items = Items.parse_obj(response.json()['data'])
            self.save_csv(items)
            offset += 50
        print("Готово")


if __name__ == '__main__':
    choose_category = (
        'электроинструмент',
        'ручной инструмент',
        'расходные материалы к электроинструменту',
        'абразивные материалы',
        'высотные конструкции',
        'расходные материалы, хозтовары',
        'спецодежда и средства защиты',
        'бензоинструмент и принадлежности',
        'газовое и сварочное оборудование',
        'измерительные инструменты',
        'силовая, строительная техника и комплектующие',
    )
    print('\n'.join(str(elem) for elem in choose_category))
    PetrovichParser(input(f"\nВведи категорию из предложенных:")).parse()
