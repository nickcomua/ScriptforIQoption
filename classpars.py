import re
import telethon
from pyquery import PyQuery as pq
from iqoptionapi.stable_api import IQ_Option
import json

# import sys
json.load
api_id = 00000 #telegram bot api_id
api_hash = ''#telegram bot api_hash 
client = telethon.TelegramClient('name_of_session', api_id, api_hash)
amount = 100
use_trail_stop = False
auto_margin_call = False
use_token_for_commission = True
I_want_money = IQ_Option("", "")#login,pass in IQoption
I_want_money.change_balance("PRACTICE")
with open("data_name_to_id.json", "r") as read_file:
    data_name_to_id = json.load(read_file)

with open("data_id_to_name.json", "r") as read_file:
    data_id_to_name = json.load(read_file)


def buy(mass):
    global I_want_money
    return I_want_money.buy_order(mass[0], mass[1], mass[2], mass[3], mass[4], mass[5], mass[6], mass[7], mass[8],
                                  mass[9], mass[10], mass[11], mass[12], mass[13], mass[14])


def write(mass, path, type='w'):
    with open(path, type) as write_file:
        json.dump(mass, write_file)


# noinspection PyBroadException
async def getinfo(funa, funwa, *args):
    ar = []
    for i in funa:
        try:
            ar += await i[0](i[1])
        except:
            continue
    for i in funwa:
        # try:
        ar += i()
        # except:
        continue
    return ar


def diff(mass1, mass2):
    ans = []
    if (not mass2) | (not mass1):
        return mass1
    for m in mass1:
        if not (m in mass2):
            ans.append(m)
    return ans


def getlaverage(active_id, buy_sell, stop_loss, type_opt="forex"):
    global I_want_money
    masslaverage = I_want_money.get_available_leverages(type_opt, active_id)[1]['leverages'][0]['regulated']
    divide0 = abs(1 - stop_loss / buy_sell)
    lavarage0 = 0
    for i in masslaverage:
        if i * divide0 < 1:
            lavarage0 = i
            continue
        break
    return lavarage0


async def getfromtela(search, *args):
    global amount, use_trail_stop, auto_margin_call, use_token_for_commission, I_want_money, client, data_id_to_name

    async for i in client.iter_messages('VipCoinexhangePump', limit=1, search=search):
        text = re.sub(r' ', '', i.text)
    t = re.split(r"[#@\n]", text)
    t[0] = re.search(r'buy|sell', i.text.lower()).group()
    t[1] = re.search('#[A-Z]+@', text).group()[1:-1]

    if not t[1] in data_id_to_name:
        return []

    action0 = t[0].lower()
    stop_loss0 = float(t[-1])
    take_profit0 = float(t[4])
    buy_sell0 = float(t[2])
    active_id0 = t[1]
    lavarage0 = getlaverage(active_id0, buy_sell0, stop_loss0)

    action1 = t[0].lower()
    stop_loss1 = float(t[-1])
    take_profit1 = float(t[8])
    buy_sell1 = float(t[6])
    active_id1 = t[1]
    lavarage1 = getlaverage(active_id0, buy_sell1, stop_loss1)

    return [
        [
            'forex', active_id0, action0, amount,
            lavarage0, 'limit', buy_sell0,
            None, "price", stop_loss0, "price", take_profit0,
            use_trail_stop, auto_margin_call, use_token_for_commission
        ],

        [
            'forex', active_id1, action1, amount,
            lavarage1, 'limit', buy_sell1,
            None, "price", stop_loss1, "price", take_profit1,
            use_trail_stop, auto_margin_call, use_token_for_commission
        ]
    ]


def getfrommt5():
    global amount, use_trail_stop, auto_margin_call, use_token_for_commission, client, data_name_to_id, data_id_to_name
    site = pq('https://mobile.mt5.com/en/signals')
    name = site.find('#quote_name').text().split()[0]
    type_of_op = 'forex'
    id = name
    if name[0] == '#':
        name = name[1:]
        if not name in data_name_to_id:
            return []
        id = data_name_to_id[name][0]
        type_of_op = data_name_to_id[name][1]
    if not id in data_id_to_name:
        return []

    action = site.find('body > main > div > div > div.block-content > div:nth-child(1) > div.block-signals__table > div:nth-child(2) > div > span').text().split()[0].lower()
    buy_sell = float(site.find('body > main > div > div > div.block-content > div:nth-child(1) > div.block-signals__tableprice > div:nth-child(3) > div').text().split()[1])
    stop_loss = float(site.find('body > main > div > div > div.block-content > div:nth-child(1) > div.block-signals__tableprice > div:nth-child(2) > div').text().split()[1])
    take_profit = float(site.find('body > main > div > div > div.block-content > div:nth-child(1) > div.block-signals__tableprice > div:nth-child(1) > div').text().split()[1])
    laverage = getlaverage(id, buy_sell, stop_loss, type_opt=type_of_op)

    return [[
        type_of_op, id, action, amount, laverage,
        'limit', buy_sell, None,
        "price", stop_loss,
        "price", take_profit,
        use_trail_stop, auto_margin_call, use_token_for_commission
    ]]
