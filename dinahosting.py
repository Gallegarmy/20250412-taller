import re
import asyncio

from playwright.async_api import async_playwright

from scraper import Scraper

SPACE_REGEX = re.compile(r'\s+')
SELECTORS = ('#TEMPLATE-RESULT-BASICOS', '#TEMPLATE-RESULT-AVANZADOS', '#TEMPLATE-RESULT-MULTIHOSTING')


async def main():
    async with async_playwright() as playwright:
        scraper = Scraper(playwright)
        url = 'https://gl.dinahosting.com/hosting/precios-hosting'  # 'https://dinahosting.com/hosting/precios-hosting'
        page = await scraper.get_page(url)

        for selector in SELECTORS:
            button_elems = await page.query_selector_all(selector + ' button')
            ul_elems = await page.query_selector_all(selector + ' ul')
            while(len(ul_elems)):
                title_button = button_elems.pop()
                await process_title(title_button)

                ul_elem = ul_elems.pop()
                li_elems = await ul_elem.query_selector_all('li')
                for li_elem in li_elems:
                    duration_elem = await li_elem.query_selector('span:nth-child(1)')
                    price_elem = await li_elem.query_selector('p')
                    print(f'{await get_clean_text(price_elem):>12} :: {await get_clean_text(duration_elem)}')


async def process_title(title_button):
    print(f"\n***** {await get_clean_text(title_button)}")

async def get_clean_text(elem):
    text = await elem.text_content()
    return SPACE_REGEX.sub(' ', text)

if __name__ == '__main__':
    asyncio.run(main())