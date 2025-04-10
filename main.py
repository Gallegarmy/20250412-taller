import re
import asyncio
from asyncio import sleep

from playwright.async_api import async_playwright, Page, Browser

SPACE_REGEX = re.compile(r'\s+')
SELECTORS = ('#TEMPLATE-RESULT-BASICOS', '#TEMPLATE-RESULT-AVANZADOS', '#TEMPLATE-RESULT-MULTIHOSTING')

class Scraper:
    def __init__(self, playwright: async_playwright):
        self.playwright = playwright
        self._browser = None

    async def _get_browser(self) -> Browser:
        if self._browser is None:
            self._browser = await self.playwright.chromium.launch(headless=True)
        return self._browser

    async def get_page(self, url: str) -> Page:
        page = await (await self._get_browser()).new_page()
        await page.goto(url)
        await sleep(1.6)
        #await page.wait_for_load_state('domcontentloaded')  # alternativa: 'load'
        return page




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