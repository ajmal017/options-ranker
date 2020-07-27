import requests
import json
from api_key import key


class Stock:
    options_endpoint = "https://finnhub.io/api/v1/stock/option-chain"
    quote_endpoint = "https://finnhub.io/api/v1/quote"
    profile_endpoint = "https://finnhub.io/api/v1/stock/profile2"

    def __init__(self, ticker):
        self.ticker = ticker
        params = {"symbol": self.ticker, "token": key}
        self.profile = requests.get(self.profile_endpoint, params=params).json()

    #returns the current price of the stock
    def current_price(self):
        payload = {"symbol": self.ticker}
        price = requests.get(self.quote_endpoint, params = payload).json()
        return price["c"]

    #returns the options chain for the stock as a JSON object
    def get_options_chain(self):
        payload = {"symbol": self.ticker, "token": key}
        chain = requests.get(self.options_endpoint, params=payload).json()
        return chain
    
    #returns the ticker
    def get_ticker(self):
        return self.ticker

    #return company logo (.png)
    def get_logo(self):
        return self.profile["logo"]
