
class Options:

    def __init__(self, options_data, ticker):
        self.options_data = options_data
        self.options_chain = self.get_options_chain()
        self.ticker = ticker

    #returns a list of 50 options with the highest volume
    def get_options_chain(self):
        options_list = []
        data = self.options_data["data"]
        for exp in range(0, len(data)):
            calls = data[exp]["options"]["CALL"]
            for contract in range(0, len(calls)):
                options_list.append(calls[contract])
            puts = data[exp]["options"]["PUT"]
            for contract in range(0, len(puts)):
                options_list.append(calls[contract])
        return options_list

    #sorts the options chain in ascending order of order == true, and descending otherwise
    def chain_sorted_volume(self, order):
        options_list = sorted(
            self.options_chain, 
            key=lambda volume: -1 if volume["volume"] is None else volume["volume"], 
            reverse=order)
        while len(options_list) > 25:
            options_list.pop()
        return options_list

    def volume_formatted(self, order):
        options = self.chain_sorted_volume(order)
        formatted_list = []
        for option in options:
            concise_data = {}
            concise_data.update(data = "{} ${} {}\nExp: {}".format(self.ticker, option["strike"], option["type"], option["expirationDate"]))
            concise_data.update(print_metric = "volume: {}".format(option["volume"]))
            formatted_list.append(concise_data)
        return formatted_list
 
    #sorts the options chain in ascending order if order == true, and descending otherwise 
    def chain_sorted_OI(self, order):
        options_list = sorted(
            self.options_chain, 
            key=lambda open_interest: -1 if open_interest["openInterest"] is None else open_interest["volume"], 
            reverse=order)
        while len(options_list) > 25:
            options_list.pop()
        return options_list

    def open_interest_formatted(self, order):
        options = self.chain_sorted_OI(order)
        formatted_list = []
        for option in options:
            concise_data = {}
            concise_data.update(data = "{} ${} {}\nExp: {}".format(self.ticker, option["strike"], option["type"], option["expirationDate"]))
            concise_data.update(print_metric = "open-interest: {}".format(option["openInterest"]))
            formatted_list.append(concise_data)
        return formatted_list




#other ideas: sort by lowest/highest premiems

