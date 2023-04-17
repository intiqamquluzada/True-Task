from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from .models import Instagram
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from accounts.models import MyUser as User


def make_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/usr/bin/chromium"

    # driver_path = '/usr/share/doc/chromium-driver'  # Set the executable path here
    PATH = '/usr/bin/chromedriver'
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    return driver


logger = get_task_logger("core")


@shared_task
def scrape_data():
    driver = make_driver()
    logger.info("Executing periodic task starting ...")
    users = User.objects.all()
    # user = get_object_or_404(User, slug=slug)
    for user in users:
        if user.instagram:
            username = user.instagram.username
            password = user.instagram.password
            driver.get('https://www.instagram.com/accounts/login/')
            time.sleep(2)
            username_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'username')))
            username_field.send_keys(username)
            print("Username field isledi")
            password_field = driver.find_element(By.NAME, 'password')
            password_field.send_keys(password)
            print("Parol field isledi")
            login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            # time.sleep(10)
            login_button.click()
            print("button isledi")
            WebDriverWait(driver, 5).until(EC.url_contains('instagram.com'))

            # Add a delay before navigating to the profile page
            # time.sleep(10)

            # Navigate to the profile page
            profile_url = f"https://www.instagram.com/{username}/"
            driver.get(profile_url)

            # Wait for the login process to complete
            # time.sleep(10)
            print("hellololololololo")
            ul = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
            print(ul)
            items = ul.find_elements(By.TAG_NAME, 'li')
            my_dict = []
            for item in items:
                print(item.text)
                my_dict.append(item.text)
            new_dict = {s.split()[1]: int(s.split()[0]) for s in my_dict}
            print(new_dict)
            driver.quit()
            try:
                instagram = user.instagram
            except ObjectDoesNotExist:
                instagram = Instagram(user=user)
            instagram.followers = int(new_dict['followers'])
            instagram.following = int(new_dict['following'])
            instagram.save()
            return instagram.followers, instagram.following



def scrape_data_copy(slug):
    driver = make_driver()
    logger.info("Executing periodic task starting ...")
    user = get_object_or_404(User, slug=slug)
    if user.instagram:
        username = user.instagram.username
        password = user.instagram.password
        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        username_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, 'username')))
        username_field.send_keys(username)
        print("Username field isledi")
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)
        print("Parol field isledi")
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        # time.sleep(10)
        login_button.click()
        print("button isledi")
        WebDriverWait(driver, 5).until(EC.url_contains('instagram.com'))

        # Add a delay before navigating to the profile page
        # time.sleep(10)

        # Navigate to the profile page
        profile_url = f"https://www.instagram.com/{username}/"
        driver.get(profile_url)

        # Wait for the login process to complete
        time.sleep(10)
        print("hellololololololo")
        ul = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
        print(ul)
        items = ul.find_elements(By.TAG_NAME, 'li')
        my_dict = []
        for item in items:
            print(item.text)
            my_dict.append(item.text)
        new_dict = {s.split()[1]: int(s.split()[0]) for s in my_dict}
        print(new_dict)
        driver.quit()
        try:
            instagram = user.instagram
        except ObjectDoesNotExist:
            instagram = Instagram(user=user)
        instagram.followers = int(new_dict['followers'])
        instagram.following = int(new_dict['following'])
        instagram.save()
        return instagram.followers, instagram.following