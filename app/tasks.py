from __future__ import absolute_import, unicode_literals
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from .models import Instagram
from django.core.exceptions import ObjectDoesNotExist



# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
#
# # driver_path = '/usr/share/doc/chromium-driver'  # Set the executable path here
# driver = webdriver.Chrome(executable_path='/usr/bin/chromium-driver', options=options)


@shared_task
def scrape_data():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for instagram in Instagram.objects.all():

        username = instagram.username
        password = instagram.password

        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username')))
        username_field.send_keys(username)
        print("Username field isledi")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password')))

        password_field.send_keys(password)
        print("PArol field isledi")
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
        )

        login_button.click()
        print("button isledi")
        WebDriverWait(driver, 10).until(EC.url_contains('instagram.com'))
        print('instagrama getdi')
        # Add a delay before navigating to the profile page

        # Navigate to the profile page
        profile_url = f"https://www.instagram.com/{username}/"
        driver.get(profile_url)
        print('profile girdi')

        # Wait for the login process to complete
        time.sleep(10)
        ul = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
        print('datalari cekir')
        items = ul.find_elements(By.TAG_NAME, 'li')
        print('datalari cekdi')
        my_dict = []
        for item in items:
            print(item.text)
            my_dict.append(item.text)
        new_dict = {s.split()[1]: int(s.split()[0]) for s in my_dict}
        print(new_dict)

        try:
            instagram = user.instagram
        except ObjectDoesNotExist:
            instagram = Instagram(user=user)
        instagram.followers = int(new_dict['followers'])
        instagram.following = int(new_dict['following'])
        instagram.save()
        driver.quit()
        return instagram.followers, instagram.following


