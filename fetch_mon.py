import asyncio
from pyppeteer import launch

from lxml import etree

async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
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
    await asyncio.sleep(20)

    # print('screeshot')
    # await page.screenshot({'path': 'after.png'})
    await page.close()
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())