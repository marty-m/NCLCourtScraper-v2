import cookie
import os
import datetime
import booking
import re
from startAlertServer import addBooking
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

def court5():
    load_dotenv()

    NCL_EMAIL = os.getenv('NCL_EMAIL')
    NCL_PASSWORD = os.getenv('NCL_PASSWORD')



    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        context.add_cookies(cookie.cookie)

        page.goto('https://sportsbookings.ncl.ac.uk/Connect/memberHomePage.aspx')
        if page.url == 'https://appspay.ncl.ac.uk/sport/Login/Index?ReturnUrl=%2fsport%2fbooking':
            # Implement Twilio SMS alert to inform of cookie expiry with outlook verification number asking for approval
            

        page.wait_for_selector('#form_1')
        page.locator('//*[@id="form_1"]/div[1]/div/a').click()
        

        page.wait_for_selector('#ctl00_ctl11_Li1')
        page.locator('//*[@id="ctl00_ctl11_Li1"]/a').click()

        page.wait_for_selector('#ctl00_MainContent_activityGroupsGrid_ctrl10_lnkListCommand')
        page.locator('//*[@id="ctl00_MainContent_activityGroupsGrid_ctrl10_lnkListCommand"]').click()

        page.wait_for_selector('#ctl00_MainContent_activitiesGrid_ctrl1_lnkListCommand')
        page.locator('//*[@id="ctl00_MainContent_activitiesGrid_ctrl1_lnkListCommand"]').click()

        for i in range(2):
            availableOnPage = page.evaluate("document.getElementsByClassName('itemofcurrentuser').length")
            
            if availableOnPage != 0:
                for j in range(availableOnPage):
                    rawCell = page.evaluate(f"document.getElementsByClassName('itemofcurrentuser')[{j}].querySelector('span > input').getAttribute('data-qa-id')")
                    date = re.search('(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|[1][0-2])/[0-9]+ [0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?', rawCell).group(0)
                    addBooking(booking.Booking(5, datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")))
            
            page.locator('//*[@id="ctl00_MainContent_dateForward1"]').click()

        browser.close()

court5()