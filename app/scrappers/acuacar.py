from app.parsers.acuacar_parser import AcuacarParser
from app.scrappers.base import BaseScraper


class AcuacarScraper(BaseScraper):
    async def scrape(self, browser):
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://acuacarapps.com:8096/AcuaFormSite/formulario/lista-mantenimientos", wait_until="networkidle")
        
        cortes = []

        filas = await page.locator("//table//tbody//tr").all()

        for fila in filas:
            nombre = await fila.locator("xpath=.//td[1]").inner_text()
            await fila.locator('xpath=.//td//button').click()   
            await page.locator("//button[1][@role='tab']").wait_for(state="visible")
            tabs = await page.locator("//button[@role='tab']").all()
            for i in range(0, len(tabs)):
                if i == 0:
                    continue
                await tabs[i].click()
            barrios = await page.locator("//div[@class='mt-5']").all()
            content = await page.content()
            data = AcuacarParser.parse_html(content)
            cortes.append(data)
            if len(filas) > 1:
                await (await page.locator("button").all())[0].click()
                await page.wait_for_load_state("networkidle")




        
        await context.close()
        return cortes