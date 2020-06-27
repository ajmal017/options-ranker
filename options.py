
class Options:

    def __init__(self, options_data):
        self.options_data = options_data
        self.options_chain = self.get_options_chain()

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

    #sorts the options chain by highest volume
    def chain_sorted_volume(self):
        options_list = sorted(
            self.options_chain, 
            key=lambda volume: -1 if volume["volume"] is None else volume["volume"], 
            reverse=True)
        while len(options_list) > 25:
            options_list.pop()
        return options_list
 
    #sorts the options chain by highes open interest
    def chain_sorted_OI(self):
        options_list = sorted(
            self.options_chain, 
            key=lambda open_interest: -1 if open_interest["openInterest"] is None else open_interest["volume"], 
            reverse=True)
        while len(options_list) > 25:
            options_list.pop()
        return options_list

