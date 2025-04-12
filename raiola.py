import re
import asyncio

from playwright.async_api import async_playwright

from scraper import Scraper

SPACE_REGEX = re.compile(r'\s+')
SELECTORS = ('#TEMPLATE-RESULT-BASICOS', '#TEMPLATE-RESULT-AVANZADOS', '#TEMPLATE-RESULT-MULTIHOSTING')


async def debug_element(page, selector):
    print("\n=== Element Debug Information ===")

    try:
        element = await page.query_selector(selector)
        print(f"Element exists: {bool(element)}")

        # Get detailed element state
        state = await page.evaluate("""
            async el => ({
                visibility: window.getComputedStyle(el).visibility,
                position: window.getComputedStyle(el).position,
                zIndex: parseInt(window.getComputedStyle(el).zIndex),
                rect: el.getBoundingClientRect(),
                offsetParent: Boolean(el.offsetParent),
                eventListeners: getEventListeners(el)
            })
        """, element)

        print("\nElement State:")
        for key, value in state.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error accessing element: {str(e)}")


async def debug_page_context(page):
    print("\n=== Page Context Information ===")

    # Check for overlays and modals
    overlays = await page.query_selector_all('body > *')
    print(f"Number of overlay elements: {len(overlays)}")

    # Check viewport size
    viewport_size = page.viewport_size
    print(f"Viewport size: {viewport_size}")

    # Check iframes
    frames = page.frames
    print(f"Number of frames: {len(frames)}")

async def main():
    async with async_playwright() as playwright:
        scraper = Scraper(playwright)
        url = 'https://raiolanetworks.com/hosting-web/'  # 'https://dinahosting.com/hosting/precios-hosting'
        page = await scraper.get_page(url)

        # Debug your element
        await debug_element(page, "#toggle")
        await debug_page_context(page)

"""
        column_elems = await page.query_selector_all('#products > div.container.relative.mx-auto.mb-20.mt-\[-100px\].max-w-screen-xl.px-4 > div > div div.product-card')
        while(len(column_elems)):
            column_elem = column_elems.pop()
            title_elem = await column_elem.query_selector(' > div > p')
            price_elem = await column_elem.query_selector(' div div.relative p')
            print(f"\n***** {await get_clean_text(title_elem)}")
            print(f'{await get_clean_text(price_elem):>12} :: ')

"""

async def get_clean_text(elem):
    text = await elem.text_content()
    return SPACE_REGEX.sub(' ', text)

if __name__ == '__main__':
    asyncio.run(main())