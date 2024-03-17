import os
import datetime
import booking
import re
from helper import send_message, get_stored_cookie, dump_cookie, store_booking, get_stored_bookings
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


def court5():
    load_dotenv()


    NCL_EMAIL = os.getenv("NCL_EMAIL")
    NCL_PASSWORD = os.getenv("NCL_PASSWORD")


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        context.add_cookies(get_stored_cookie())

        page.goto('https://sportsbookings.ncl.ac.uk/Connect/memberHomePage.aspx')

        if page.query_selector('#ctl00_ctl11_Li1') is None:
            page.wait_for_selector('#form_1')
            page.locator('//*[@id="form_1"]/div[1]/div/a').click()

        while page.url == 'https://appspay.ncl.ac.uk/sport/Login/Index?ReturnUrl=%2fsport%2fbooking':
            page.wait_for_selector('#Authenticate')
            page.locator('//*[@id="Authenticate"]/fieldset/div[1]/div[2]/a').click()
            
            page.wait_for_timeout(3000)
            if page.url == 'https://sportsbookings.ncl.ac.uk/Connect/memberHomePage.aspx':
                break
            
            if page.query_selector('#idChkBx_SAOTCAS_TD') is None:
                page.wait_for_selector('#i0116')
                page.fill('#i0116', NCL_EMAIL)
                page.click('#idSIButton9')

                page.wait_for_selector('#i0118')
                page.fill('#i0118', NCL_PASSWORD)
                page.click('#idSIButton9')
            
            while page.url != 'https://sportsbookings.ncl.ac.uk/Connect/memberHomePage.aspx':
                page.wait_for_selector('#idChkBx_SAOTCAS_TD')
                page.check('#idChkBx_SAOTCAS_TD')
                approval = page.locator('//*[@id="idRichContext_DisplaySign"]').text_content()
                
                send_message("COOKIE EXPIRED" ,f"Code: {approval}\n\nThe court scraper cookie has expired. Please approve the login request on your phone.",priority=1)
                
                while page.is_visible('#idRichContext_DisplaySign'):
                    page.wait_for_timeout(1000)
                
                page.wait_for_timeout(4000)
                if page.is_visible('//*[@id="idA_SAASDS_Resend"]'):
                    
                    while datetime.datetime.now().hour > 23 or datetime.datetime.now().hour < 8:
                        page.wait_for_timeout(600000)

                    page.click('//*[@id="idBtn_SAASDS_Cancel"]')
                    page.wait_for_selector('//*[@id="tilesHolder"]/div[1]/div/div[1]')
                    page.click('//*[@id="tilesHolder"]/div[1]/div/div[1]')
                    continue
                if page.is_visible('#idSIButton9'):
                    page.click('#idSIButton9')
                
                page.wait_for_timeout(10000)
                
        dump_cookie(context.cookies())

        page.wait_for_selector('#ctl00_ctl11_Li1')
        page.locator('//*[@id="ctl00_ctl11_Li1"]/a').click()

        page.wait_for_selector('#ctl00_MainContent_activityGroupsGrid_ctrl10_lnkListCommand')
        page.locator('//*[@id="ctl00_MainContent_activityGroupsGrid_ctrl10_lnkListCommand"]').click()

        page.wait_for_selector('#ctl00_MainContent_activitiesGrid_ctrl1_lnkListCommand')
        page.locator('//*[@id="ctl00_MainContent_activitiesGrid_ctrl1_lnkListCommand"]').click()

        for i in range(3):
            page.wait_for_timeout(1500)
            availableOnPage = page.evaluate("document.getElementsByClassName('itemavailable').length")
            
            if availableOnPage != 0:
                for j in range(availableOnPage):
                    rawCell = page.evaluate(f"document.getElementsByClassName('itemavailable')[{j}].querySelector('span > input').getAttribute('data-qa-id')")
                    date = re.search('(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|[1][0-2])/[0-9]+ [0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?', rawCell).group(0)
                    store_booking(booking.Booking(5, datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")))
            
            page.locator('//*[@id="ctl00_MainContent_dateForward1"]').click()

        browser.close()