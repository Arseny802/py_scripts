import os


def create_html(url):
    URL = ''
    for char in url:
        if (char != '.' and char != '%' and char != '/'):
           URL += char
    expansion = ".html"
    base_addr = os.path.abspath('book.py')
    addr = ''
    if URL[4] == 's':
        addr = base_addr[:len(base_addr)-len('book.py')] + URL[6:] + expansion
    else:
        addr = base_addr[:len(base_addr)-len('book.py')] + URL[5:] + expansion
    response = "torify curl " + url + " > " + addr
    print(response)
    os.system(response)


def create_request(search_for):
    flib_search = "http://www.flibustahezeous3.onion/booksearch?ask="
    result_search = ''
    for char in search_for:
        if char == ' ':
            result_search += '%20'
        else:
            result_search += char
    return flib_search + result_search


def main():
    print("Starting...")

    ipURL = "https://2ip.ru"
    flibURL = "http://www.flibustahezeous3.onion"
    base_search = "some book name"

    create_html(ipURL)
    create_html(flibURL)
    create_html(create_request(base_search))

    print("End.")


if __name__ == "__main__":
    main()
