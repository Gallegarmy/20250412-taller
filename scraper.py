from asyncio import sleep

from playwright.async_api import async_playwright, Browser, Page


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
