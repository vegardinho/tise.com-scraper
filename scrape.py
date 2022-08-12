# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from scrape_tools import scrape_site
import arrow

PUSHOVER_TOKEN = 'ajj9psad24omqp5bmu58snhgk158mr'
TISE_REQUESTS_BASE = 'https://tise.com/'
TITLE = 'Tise.com'


def main():
    scrape_site(get_elements, get_attrs, get_next_page, TITLE, ad_string_format,
                pushover_token=PUSHOVER_TOKEN, json_request=True)


def get_elements(json):
    return json["results"]


def get_next_page(page, _page_url):
    if page["next"]:
        return urljoin(TISE_REQUESTS_BASE, page["next"])
    return None


def get_attrs(ad_element, ad_dict, search):
    ad_id = ad_element["id"]
    title = ad_element["title"]
    date_created = arrow.get((ad_element["createdAt"])).format('DD.MM.YYYY')
    price = ad_element["price"]
    seller = ad_element["userFullName"]
    href = ad_element["buttons"][0]["universalLink"][:-4]
    description = ad_element["caption"]
    subtitle = ad_element["spec1"]
    address = ad_element["posName"]

    ignore = ['ønsker', 'ønsket', 'ønskes']
    for e in ignore:
        if e in subtitle.lower():
            return ad_dict


    ad_dict[ad_id] = dict(
        href=href,
        title=title,
        subtitle=subtitle,
        description=description,
        address=address,
        price=price,
        search=search,
        seller=seller,
        date_created=date_created
    )

    return ad_dict


def ad_string_format(ad_link, search_link, ad_dict):
    return f'{ad_link} – {ad_dict["price"]},- ({search_link})\n{ad_dict["subtitle"]} ({ad_dict["seller"]})\n\
    {ad_dict["date_created"]} – {ad_dict["address"]}\n'


if __name__ == '__main__':
    main()
