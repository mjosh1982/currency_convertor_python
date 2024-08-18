# write your code here!
import requests


class CurrenCyConvertor:

    def __init__(self, from_curr, to_curr):
        self.rates = {}
        self.rate_count = {}
        self.from_currency_code = from_curr
        self.to_currency_code = to_curr
        self.url = 'https://www.floatrates.com/daily/{}.json'.format(self.from_currency_code.lower())
        self.response = None
        # self.load_rates(value)
        self.cache_rates(self.get_currency_from_json())

    def load_rates(self, key, value):
        return self.rates[key] * value

    def display_message(self):
        value = float(input())
        for k, v in self.rates.items():
            print(f'I will get {round(self.load_rates(k, value), 2)} {k} from the sale of {float(value)} conicoins.')

    def get_currency_from_json(self, url=None):
        if url == None:
            url = self.url
        if self.response is None:
            self.response = requests.get(url)

        return self.response.json()

    def get_currency_tag(self, data, currency):
        return data.get(currency)

    def cache_currency(self, currency, value):
        self.rates[currency] = value

    def cache_rates(self, data):
        for k, v in data.items():

            self.rate_count[k] = 0.0

            if k == 'usd' or k == 'eur':
                self.cache_currency(k, v['rate'])

    def get_rates(self):
        return self.rates

    def get_rate_for_currency(self, data, currency):
        print('Checking the cache...')
        if currency.lower() in self.rates:
            print('Oh! It is in the cache!')
            self.rate_count[currency] = self.rates[currency] + 1
            return self.rates[currency]
        else:
            print('Sorry, but it is not in the cache!')
            self.rates[currency] = data.get(currency)['rate']
            self.rate_count[currency] = 0
            return data.get(currency)['rate']

    def set_to_curr(self, currency):
        self.to_currency_code = currency


from_curr = input()
to_curr = ''
cc = CurrenCyConvertor(from_curr, None)

while True:
    from_curr = from_curr.lower()
    to_curr = input()
    if to_curr == '':
        break
    to_curr = to_curr.lower()
    cc.set_to_curr(to_curr)
    value = input()
    data = cc.get_currency_from_json()
    rate = cc.get_rate_for_currency(data, to_curr)
    val = float(value) * rate
    print(f'You received {round(val, 2)} {to_curr.upper()}.')
