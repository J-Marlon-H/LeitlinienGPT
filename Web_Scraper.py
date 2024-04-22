import asyncio
from playwright.async_api import async_playwright
import aiohttp
import aiofiles
import asyncio
import os
import re

# The function to download the file
async def download_file(url, folder, name):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, name)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await resp.read())
                print(f"Downloaded {name} to {folder}")
            else:
                print(f"Failed to download {url}. Status code: {resp.status}")

async def run():
    download_folder = 'Database'
    Final_Link_List = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Use headless=False to see the browser UI
        context = await browser.new_context()
        context.set_default_timeout(120000)
        page = await context.new_page()

        # Navigate to the page
        await page.goto('https://register.awmf.org/de/leitlinien/aktuelle-leitlinien')

        # Wait for the list under "NACH FACHGESELLSCHAFT" to load
        await page.wait_for_selector('ion-col.guideline-listing-title.md.hydrated')

        # Wait for the "NACH FACH" tab to be available and click on it
        await page.click('ion-segment-button[value="discipline"]')

        # Wait for the list under "NACH FACH" to load
        await page.wait_for_selector('ion-col.guideline-listing-title.md.hydrated')

        # Collect all link URLs
        link_elements = await page.query_selector_all('ion-col.guideline-listing-title.md.hydrated a')
        main_links = []
        Fachgesellschaften= []
        for link_element in link_elements:
            href = await link_element.get_attribute('href')
            Fachgesellschaft = await link_element.text_content()
            main_links.append(href)
            Fachgesellschaften.append(Fachgesellschaft)
        print("main_links:", len(main_links))
        print("Fachgesellschaften: ",len(Fachgesellschaften))

        # Loop through the collected links and click on each one
        for i in range(len(main_links)):
            # Navigate to the link
            print(f'main_link: https://register.awmf.org{main_links[i]}')
            await page.goto(f'https://register.awmf.org{main_links[i]}')
            await page.wait_for_load_state('networkidle')

            # Locate the h3 header
            header = await page.query_selector('h3:text("Beteiligungen an Leitlinien anderer Fachgesellschaften")')

            # Get the y-coordinate of the header
            header_box = await header.bounding_box() if header else None
            header_y = header_box['y'] if header_box else float('inf')

            # Collect sub_links only above the h3 header
            sub_link_elements = await page.query_selector_all('ion-col.guideline-listing-title.md.hydrated a')
            sub_links = []
            for sub_link in sub_link_elements:
                sub_link_box = await sub_link.bounding_box()
                if sub_link_box is None:
                    break
                if sub_link_box['y'] < header_y:
                    href = await sub_link.get_attribute('href')
                    sub_links.append(href)
            print("sub_links:", len(sub_links))
            
            for sub_link in sub_links:
                await page.wait_for_load_state('networkidle')
                print("sub_link:", sub_link)
                # Click on sub-link and wait for navigation
                await page.goto(sub_link)

                first_download_button = page.locator('text=Download').first

                # Retrieve the 'href' attribute of the first download button
                download_href = await first_download_button.get_attribute('href')

                Final_Link_List.append(download_href)

                # You can customize the file name here
                file_name_tmp = download_href.rsplit('/', 1)[-1]
                file_name = f"{Fachgesellschaften[i]}__{file_name_tmp}"  # Change this to your preferred file naming convention
                print("file_name:", file_name)

                final_link = f"https://register.awmf.org{download_href}"
                print("final_link:", final_link)

                # Call the download function
                
                
                await download_file(final_link, download_folder, file_name)


                await page.go_back()
            await page.go_back()
        print(Final_Link_List)
        print(len(Final_Link_List))

        # Close the browser
        await browser.close()

# The entry point for the script execution
if __name__ == '__main__':
    asyncio.run(run())
