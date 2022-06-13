import asyncio
from pyppeteer import launch
import json

from lxml import etree

counter = 0

async def intercept_network_response(response):
    global counter
    if "application/json" in response.headers.get("content-type", ""):
        # # Print some info about the responses
        if ('query2' in response.url):
            # ignore the first response
            counter += 1
            
            if counter > 1:
                try:
                    # await response.json() returns the response as Python object
                    # a dict
                    content = await response.json()

                    f = open(str(counter)+".txt", "a")
                    
                    f.write(str(response.url) + '\r\n' + str(response.headers) + '\r\n' + \
                            str(response.request.headers) + '\r\n' + str(content))
                    f.close()
                except json.decoder.JSONDecodeError:
                    # NOTE: Use await response.text() if you want to get raw response text
                    print("Failed to decode JSON from", await response.text())

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    page.on('response', lambda response: asyncio.ensure_future(intercept_network_response(response)))
    await page.goto('https://sgpokemap.com/index.html')

    # ## get local storage
    # local_storage = await page.evaluate('''() =>  Object.assign({}, window.localStorage)''')
    # print(local_storage)

    # print('setup localStorage, which pokemon to ignore')

    ## $('#deselect_all_btn').bind('click', function()
    cmd_str = \
    '''
    for (var key in pokeDict) {
        uncheckPokemon(key);
      }
    '''
    # for i in range(890):
    #     cmd_str += "localStorage.setItem('" + str(i) + "', '0');"

    

    search_list = [211]
    # search_list.append(304)
    for pokemon_id in search_list:
        cmd_str += 'checkPokemon(' + str(pokemon_id) + ');'

    cmd_str += \
    '''
    generateFilterList();
    inserted = 0;
    var firstTime = false;
    reloadPokemons(firstTime);
    '''
            
    await page.evaluate(cmd_str)
    # local_storage = await page.evaluate('''() =>  Object.assign({}, window.localStorage)''')
    # print(local_storage)

    print('sleep for 5 secs')
    await asyncio.sleep(30)

    # print('screeshot')
    # await page.screenshot({'path': 'after.png'})
    await page.close()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())