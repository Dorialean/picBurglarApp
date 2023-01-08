from typing import List
from http.client import IncompleteRead
from bs4 import BeautifulSoup


def get_picture_links_by_page(base_url: str, page_num: int) -> List[str]:
    base_url += f"?pageNum={page_num}"
    html = open_page(base_url)
    soup = BeautifulSoup(html, "html.parser")
    return get_page_picture_links(soup)


def open_page(url):
    from urllib.request import urlopen
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return html


def get_page_picture_links(souped_page: BeautifulSoup) -> List[str]:
    linkTags = souped_page.find_all("a", href=True)
    all_valid_links = []
    for linkTag in linkTags:
        if str(linkTag['href']).startswith('/app/masterpiece/'):
            all_valid_links.append(linkTag['href'])
    return all_valid_links


def get_img_link(souped_page: BeautifulSoup) -> str:
    div = souped_page.find("div", class_="masterpiece-head-image")
    img = div.findChild('img')
    return img['src']


def get_page_amount(souped_page) -> int:
    div = souped_page.find('div', class_="pagination")
    if div is not None:
        nav_links = div.findAll('a', href=True)
        max_page = 0
        for nav_link in nav_links:
            link_href = str(nav_link["href"])
            if link_href.startswith("/app/gallery?pageNum="):
                page_num = int(link_href[link_href.index('=') + 1:])
                if page_num > max_page:
                    max_page = page_num
        return max_page


def download_image(url, file_path, file_name):
    import urllib.request as req
    full_path = file_path + file_name + '.jpg'
    req.urlretrieve(url, full_path)


def main():
    base_url = 'https://my.tretyakov.ru'
    base_gallery_url = 'https://my.tretyakov.ru/app/gallery'
    saving_path = 'src/imgs/'

    html = open_page(base_gallery_url)
    soup = BeautifulSoup(html, "html.parser")

    for p in range(1, get_page_amount(soup)):
        for link in get_picture_links_by_page(base_gallery_url, p):
            try:
                html = open_page(base_url + link)
            except IncompleteRead:
                continue
            soup = BeautifulSoup(html, "html.parser")
            img_save_link = get_img_link(soup)
            download_image(img_save_link, saving_path, img_save_link.split('/')[-1].split('.')[0])


if __name__ == '__main__':
    main()
