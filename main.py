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
        #await sleep(1.6)
        return page




async def main():
    async with async_playwright() as playwright:
        scraper = Scraper(playwright)
        page = await scraper.get_page('https://dinahosting.com/hosting/precios-hosting')
        await page.wait_for_load_state('load')

        for selector in SELECTORS:
            button_elems = await page.query_selector_all(selector + ' button')
            ul_elems = await page.query_selector_all(selector + ' ul')
            while(len(ul_elems)):
                title_button = button_elems.pop()
                title_text = await title_button.text_content()
                print(f"***** {SPACE_REGEX.sub(' ', title_text)}", end='')

                ul_elem = ul_elems.pop()
                li_elems = await ul_elem.query_selector_all('li')
                for li_elem in li_elems:
                    elem_text = await li_elem.text_content()
                    print(SPACE_REGEX.sub(' ', elem_text))


if __name__ == '__main__':
    asyncio.run(main())