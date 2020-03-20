import asyncio
import classpars
import time

ar = []
im = []


async def main():
    global ar, im
    mass = []
    funa = [[classpars.getfromtela, 'buy'], [classpars.getfromtela, 'sell']]
    funwa = [classpars.getfrommt5]
    ar += await asyncio.ensure_future(classpars.getinfo(funa, funwa))
    print('start')
    while True:
        im = await asyncio.ensure_future(classpars.getinfo(funa, funwa))
        diff = classpars.diff(im, ar)
        if diff:
            ar += im
            classpars.write(ar, 'logs.json')
            for i in diff:
                print(i)
                mass.append(classpars.buy(i)+time.time())
                classpars.write(mass, 'ids.json')
        await asyncio.sleep(30)


with classpars.client:
    classpars.client.loop.run_until_complete(main())
