import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Use headless=False to see the browser UI
        page = await browser.new_page()

        # Navigate to the page
        await page.goto('https://register.awmf.org/de/leitlinien/aktuelle-leitlinien')

        # Wait for the list under "NACH FACHGESELLSCHAFT" to load
        await page.wait_for_selector('ion-col.guideline-listing-title.md.hydrated', timeout=60000)

        # Wait for the "NACH FACH" tab to be available and click on it
        await page.click('ion-segment-button[value="discipline"]')

        # Wait for the list under "NACH FACH" to load
        await page.wait_for_selector('ion-col.guideline-listing-title.md.hydrated', timeout=60000)

        # Collect all link URLs
        link_elements = await page.query_selector_all('ion-col.guideline-listing-title.md.hydrated a')
        main_links = []
        for link_element in link_elements:
            href = await link_element.get_attribute('href')
            main_links.append(href)
        print(main_links[0])

        # Loop through the collected links and click on each one
        for link in main_links:
            # Navigate to the link
            await page.goto(f'https://register.awmf.org{link}')
            await asyncio.sleep(1)
            
            # # Get all sub-links on the current page
            # sub_links_test = await page.query_selector_all('ion-col.guideline-listing-row.md.hydrated a')
            # print(sub_links_test)

            #             # Collect all sub-link URLs
            # sub_links = await page.query_selector_all('ion-col.guideline-listing-row a')
            # sub_links_urls = [await link.get_attribute('href') for link in sub_links]
            # print(sub_links_urls)

            # # Collect all hyperlinks with the class '_ngcontent-som-c55'
            # link_elements = await page.query_selector_all('a._ngcontent-som-c55')
            # print(link_elements)

            sub_links = await page.query_selector_all('ion-col.guideline-listing-title.md.hydrated a')
            print(sub_links)
            # guideline-listing-title md hydrated

            for sub_link in sub_links:
                print(sub_link)
                # Click on sub-link and wait for navigation
                await sub_link.click()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(1)  # Wait for one second
                await page.mouse.wheel(0, 100)
    	        #await asyncio.sleep(1)
                await page.wait_for_load_state('networkidle')
                
                page.locator("ion-content[class='md.hydrated'] #Download")
                # try:
                #     sub_link = await page.wait_for_selector('ion-app.md.ion-page.hydrated', state='attached')
                #     await sub_link.click()
                # except playwright.async_api.Error as e:
                #     print(f'An error occurred: {e}')
                #     # Additional logic to handle the error, maybe retry or log the occurrence for further investigation.

                # 'ion-app.md.ion-page.hydrated'
                # 'ion-content.md.hydrated'
                # 'ion-router-outlet.menu-content menu-content-overlay hydrated'
                # 'ion-router-outlet.hydrated'
                # 'ion-content.md.hydrated'
                # 'ion-grid.md.hydrated'
                # 'ion-row.md.hydrated'
                # 'ion-col.md.hydrated'
                # 'ion-grid.search_result.search_result_compact.no-bottomline.document-list.md.hydrated'
                # 'ion-row.md.hydrated'
                # 'ion-col.md.hydrated'

                # Execute a script that pierces through the shadow roots to click the button
                # await page.evaluate("""() => {
                #     let shadowRoot = document.querySelector('ion-app.md.ion-page.hydrated').shadowRoot;
                #     console.log('First level shadow root:', shadowRoot);
                #     if (!shadowRoot) {
                #         console.error('First level shadow root not found');
                #         return;
                #     }

                #     // Assuming you have an array of selectors that lead to the shadow DOM hierarchy
                #     const selectors = [
                #         'ion-content.md.hydrated',
                #         'ion-router-outlet.menu-content.menu-content-overlay.hydrated',
                #         'ion-router-outlet.hydrated',
                #         'ion-content.md.hydrated',
                #         'ion-grid.md.hydrated',
                #         'ion-row.md.hydrated',
                #         'ion-col.md.hydrated',
                #         'ion-grid.search_result.search_result_compact.no-bottomline.document-list.md.hydrated',
                #         'ion-row.md.hydrated',
                #         'ion-col.md.hydrated'
                #     ];

                #     selectors.forEach((selector, index) => {
                #         if (shadowRoot) {
                #             const nextLevel = shadowRoot.querySelector(selector);
                #             console.log(`Level ${index + 1} shadow root:`, nextLevel);
                #             if (nextLevel) {
                #                 shadowRoot = nextLevel.shadowRoot;
                #             } else {
                #                 console.error(`Selector not found or no shadowRoot available for this level: ${selector}`);
                #                 // Breaking out of the forEach loop since it doesn't support return
                #                 return false;
                #             }
                #         }
                #     });

                #     // Attempt to find and click the download button after traversing all shadow roots
                #     let downloadButton = shadowRoot.querySelector('a[download]');
                #     console.log('Download button:', downloadButton);

                #     if (downloadButton) {
                #         downloadButton.click();
                #     } else {
                #         console.error('Download button not found');
                #     }
                # }""");



        # Close the browser
        await browser.close()

# The entry point for the script execution
if __name__ == '__main__':
    asyncio.run(run())
