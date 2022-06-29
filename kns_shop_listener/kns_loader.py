from concurrent.futures import ThreadPoolExecutor

import requests
import time

if __package__:
    from .. import common
else:
    import os
    import sys
    sys.path.append(os.path.dirname(__file__) + '/..')

from common.log import get_logger

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

from record import ComputerComponents, Record

max_thread_amount = 1
component_links = {
    ComputerComponents.Motherboard: 'https://www.kns.ru/product/materinskaya-plata-msi-meg-z690-unify-x/characteristics/',
    ComputerComponents.VideoCard: 'https://www.kns.ru/product/videokarta-palit-nvidia-geforce-rtx-3090-24gb-ned3090019sb-132ba/',
    ComputerComponents.Processor: 'https://www.kns.ru/product/processor-intel-core-i9-12900kf-oem/',
    ComputerComponents.RAM1: 'https://www.kns.ru/product/operativnaya-pamyat-kingston-fury-beast-kf548c38bbk2-32/',
    ComputerComponents.RAM2: 'https://www.kns.ru/product/operativnaya-pamyat-kingston-fury-beast-kf548c38bbk2-32/',
    ComputerComponents.ROM1: 'https://www.kns.ru/product/ssd-disk-samsung-970-evo-1tb-mz-v7s1t0bw/',
    ComputerComponents.ROM2: 'https://www.kns.ru/product/ssd-disk-samsung-970-evo-plus-2tb-mz-v7s2t0bw/',
    ComputerComponents.Cooler: 'https://www.kns.ru/product/kuler-corsair-icue-h100i-elite-lcd-display-cw-9060061-ww/',
    ComputerComponents.PowerBlock: 'https://www.kns.ru/product/blok-pitaniya-thermaltake-850w-ps-spr-0850fpcbeu-r/',
    ComputerComponents.Corpus: 'https://www.kns.ru/product/korpus-zalman-n2/',
    ComputerComponents.Monitor1: 'https://www.kns.ru/product/monitor-asus-tuf-gaming-vg28uql1a/characteristics/',
    ComputerComponents.Monitor2: 'https://www.kns.ru/product/monitor-asus-tuf-gaming-vg28uql1a/characteristics/',
    ComputerComponents.Monitor3: 'https://www.kns.ru/product/monitor-asus-rog-strix-xg49vq/characteristics/',
    ComputerComponents.AudioSystem: 'https://www.kns.ru/product/audiotehnika-ecler-arqis-110bk/',
    ComputerComponents.AudioCard: 'https://www.kns.ru/product/zvukovaya-karta-creative-sb-audigy-rx-70sb155000001/otzyvy/',
}


def log():
    return get_logger('kns_loader', 'kns_shop_listener')


def download_item_page(link: str):
    try:
        with requests.Session() as session:
            result = session.get(link)
        log().info(f"Result of downloading info by link '{link}' is {result.status_code}.")
        return result.content.decode(result.encoding)
    except Exception as exception:
        log().error(f"Exception occurred on HTML downloading: {exception}")


def download_item_price(item_key: ComputerComponents):
    link: str = component_links[item_key]
    if link is None or link == "":
        log().warning(f"No link provided ti get price of '{item_key.value}'.")
        return 0

    log().info(f"Using link '{link}' to download '{item_key.value}' price.")
    page = download_item_page(link)
    if page is None or page == "":
        log().warning(f"HTML page was not downloaded for link '{link}'!")
        return 0
    log().debug(f"HTML page was successfully downloaded for link '{link}'.")

    # Workaround throw connection refuse from web-site
    if max_thread_amount <= 1:
        time.sleep(10)

    try:
        parsed_html = BeautifulSoup(page, features='html.parser')
        price_value = parsed_html.body.find('span', attrs={'class': 'price-val'}).text
        return int(price_value)
    except Exception as exception:
        log().error(f"Exception occurred on HTML parsing: {exception}")
    return 0


def download_record():
    record = Record()
    futures = []
    with ThreadPoolExecutor(max_workers=max_thread_amount) as executor:
        for component in ComputerComponents:
            futures.append((component, executor.submit(download_item_price, component)))

    for component, future_price in futures:
        log().info(f"Downloaded {future_price.result()} price for '{component.value}'.")
        record.add(component, future_price.result())
    log().info(f"Downloaded record total price: {record.total_price}.")
    return record
