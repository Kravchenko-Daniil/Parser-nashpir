import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import json
import lxml
from PIL import Image
import os
import numpy as np


requests_url1 = 'https://nashpir.ru/product-category/osetinskie-pirogi/'
requests_url2 = 'https://nashpir.ru/product-category/sdobnye-pirogi/'
requests_url4 = 'https://nashpir.ru/product-category/napitki/'


class GetContentFromSite:
    def __init__(self, url):
        self.url = url

        self.get_source_html(self.url)

        print('Complete!')

    def get_source_html(self, url):
        try:
            response = requests.get(url)
            name = f'{url.split("/")[-2]}'
            with open(f'components/Site Pages/{name}.html', 'w', encoding='utf-8') as file:
                file.write(response.text)
        except Exception as e:
            print(e)

        if self.url == requests_url1:
            self.get_content1(name)
        elif self.url == requests_url2:
            self.get_content2(name)
        elif self.url == requests_url4:
            self.get_content3(name)

    def get_content1(self, name):
        with open(f'components/Site Pages/{name}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        images = []
        for item in soup.find_all('div', class_='product-loop-images'):
            img = item.find('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
            images.append(img['src'])

        titles = []
        for item in soup.find_all('h2', class_='woocommerce-loop-product__title'):
            title = item.text
            titles.append(title)

        subtitles = []
        for item in soup.find_all('p'):
            subtitle = item.text
            subtitles.append(subtitle)
        subtitles.pop(0)

        weight = []
        for item in soup.find_all('span', class_='swatch__tooltip'):
            w = item.text
            weight.append(w.replace(' ', ''))
        weight_np = np.split(np.array(weight), len(weight)/2)
        weight = [i.tolist() for i in weight_np]

        prices = []
        for item in soup.find_all('span', class_="woocommerce-Price-amount amount"):
            price = item.text
            price = ''.join(i for i in price if i.isdecimal())+'р'
            prices.append(price)

            if price == '750р':
                prices.append('950р')
            elif price == '650р':
                prices.append('850р')
            elif price == '600р':
                prices.append('790р')
            elif price == '700р':
                prices.append('890р')
            elif price == '950р':
                prices.append('1300р')
            elif price == '1100р':
                prices.append('1400р')

        prices.pop(0)
        prices_np = np.split(np.array(prices), len(prices) / 2)
        prices = [i.tolist() for i in prices_np]

        with open(f'components/Results/{name}.json', 'w', encoding='utf-8') as file:
            data = {}
            for t, s, i, w, p in zip(titles, subtitles, images, weight, prices):
                data[t] = s, i, w, p

            json.dump(data, file, indent=4, ensure_ascii=False)

        self.collect_images(name)

    def get_content2(self, name):
        with open(f'components/Site Pages/{name}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        images = []
        for item in soup.find_all('div', class_='product-loop-images'):
            img = item.find('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
            images.append(img['src'])

        titles = []
        for item in soup.find_all('h2', class_='woocommerce-loop-product__title'):
            title = item.text
            titles.append(title)

        weight = []

        subtitles = []
        for item in soup.find_all('p'):
            subtitle = item.text
            w = subtitle.split('/')[-1].replace(' ', '')
            weight.append(w)
            subtitles.append(subtitle.split('/').pop(0).strip())
        subtitles.pop(0)

        weight.pop(0)

        prices = []
        for item in soup.find_all('span', class_="woocommerce-Price-amount amount"):
            price = item.text
            price = ''.join(i for i in price if i.isdecimal()) + 'р'
            prices.append(price)
        prices.pop(0)

        with open(f'components/Results/{name}.json', 'w', encoding='utf-8') as file:
            data = {}
            for t, s, i, w, p in zip(titles, subtitles, images, weight, prices):
                data[t] = s, i, w, p

            json.dump(data, file, indent=4, ensure_ascii=False)

        self.collect_images(name)

    def get_content3(self, name):
        with open(f'components/Site Pages/{name}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        images = []
        for item in soup.find_all('div', class_='product-loop-images'):
            img = item.find('img', class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
            images.append(img['src'])

        titles = []
        for item in soup.find_all('h2', class_='woocommerce-loop-product__title'):
            title = item.text
            titles.append(title)

        prices = []
        for item in soup.find_all('span', class_="woocommerce-Price-amount amount"):
            price = item.text
            price = ''.join(i for i in price if i.isdecimal()) + 'р'
            prices.append(price)
        prices.pop(0)

        with open(f'components/Results/{name}.json', 'w', encoding='utf-8') as file:
            data = {}
            for t, i, p in zip(titles, images, prices):
                data[t] = i, p

            json.dump(data, file, indent=4, ensure_ascii=False)

        self.collect_images(name)

    def collect_images(self, name):
        with open(f'components/Results/{name}.json', encoding='utf-8') as file:
            data = json.load(file)

            for x, y in data.items():
                img_name = y[0].split('/')[-1]
                req = requests.get(y[0]).content

                with open(f'components/Results/images1/{img_name}', 'wb') as folder:
                    folder.write(req)

                rewrite_file = open(f'components/Results/{name}.json', 'w', encoding='utf-8')

                os.chdir('components/Results/images1')
                for i in os.listdir():
                    if data[x][0].split('/')[-1] == i:
                        data[x][0] = os.path.abspath(i)
                os.chdir('../../..')

                json.dump(data, rewrite_file, ensure_ascii=False, indent=4)

        self.convert_images()

    def convert_images(self):
        folder = 'components/Results/images1'

        os.chdir(folder)
        for i in os.listdir(os.curdir):
            image = Image.open(i)
            new_image = image.resize((400, 400))
            new_image.save(i)


requests_url3 = 'https://vk.com/market-215454826'
login = 'your login'
password = 'your password'


class VkBot:
    def __init__(self, url):
        self.url = url

        self.service = Service("Components/chromedriver_win32/chromedriver.exe")
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        self.authorization(self.url)

        self.driver.close()
        self.driver.quit()

    def authorization(self, url):
        try:
            self.driver.get(url)

            time.sleep(1)

            btn_auth = self.driver.find_element(By.CLASS_NAME, 'quick_login_button.flat_button.button_wide')
            btn_auth.click()

            time.sleep(2)

            input_login = self.driver.find_element(By.CLASS_NAME, 'VkIdForm__input')
            input_login.send_keys(login)
            self.driver.find_element(By.CLASS_NAME, 'FlatButton__in').click()

            time.sleep(2)

            input_password = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/form/div[1]/div[3]/div[1]/div/input')
            input_password.send_keys(password)
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/form/div[2]/button').click()

            time.sleep(2)

            input_code = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/form/div[3]/div/div/input')
            input_code.send_keys(input('Enter your confirmation code: '))
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/form/div[4]/div/button[1]').click()

            time.sleep(2)

        except Exception as e:
            print(e)

        self.deleting_goods()

    def goods_loading(self):
        files = []
        for i in os.listdir('components/Results'):
            if os.path.splitext(i)[-1] == '.json':
                files.append(i)
        file1 = open(f'components/Results/{files[1]}', encoding='utf-8')
        file2 = open(f'components/Results/{files[2]}', encoding='utf-8')
        file3 = open(f'components/Results/{files[0]}', encoding='utf-8')
        data1 = json.load(file1)
        data2 = json.load(file2)
        data3 = json.load(file3)

        btn_add = self.driver.find_element(By.ID, 'market_add_item_btn')
        btn_add.click()

        time.sleep(2)

        # for i, k in data1.items():
        #     self.driver.find_element(By.XPATH, '//*[@id="item_name"]').send_keys(i)
        #     self.driver.find_element(By.XPATH, '//*[@id="item_sku"]').send_keys('Осетинский пирог')
        #     self.driver.find_element(By.XPATH, '//*[@id="item_description"]').send_keys(f'В наличиии\nПирог весом {k[2][0]} ({k[3][0]})\nБольшой пирог весом {k[2][1]} ({k[3][1]})\nСостав:\n{k[0]}')
        #     self.driver.find_element(By.XPATH, '//*[@id="item_link"]').send_keys('https://nashpir.ru/product-category/osetinskie-pirogi/')
        #     self.driver.find_element(By.XPATH, '//*[@id="item_price"]').send_keys(int(k[3][0][:-1]))
        #     self.driver.find_element(By.XPATH, '//*[@id="item_weight"]').send_keys(int(k[2][0][:-1]))
        #     time.sleep(2)
        #     self.driver.find_element(By.XPATH, '//*[@id="market_ei_main_photo_upload"]/input').send_keys(k[1])
        #     time.sleep(2)
        #     self.driver.find_element(By.XPATH, '//*[@id="market_photo_crop_done"]').click()
        #     time.sleep(2)
        #     self.driver.find_element(By.XPATH, '//*[@id="box_layer"]/div[2]/div/div[3]/div[1]/div[1]/button[2]').click()
        #     time.sleep(2)
        #     self.driver.find_element(By.ID, 'market_add_item_btn').click()
        #     time.sleep(2)
        #
        # for i, k in data2.items():
        #     self.driver.find_element(By.XPATH, '//*[@id="item_name"]').send_keys(i)
        #     self.driver.find_element(By.XPATH, '//*[@id="item_sku"]').send_keys('Осетинский пирог')
        #     self.driver.find_element(By.XPATH, '//*[@id="item_description"]').send_keys(f'В наличиии\nПирог весом {k[2]} ({k[3]})\nСостав:\n{k[0]}')
        #     self.driver.find_element(By.XPATH, '//*[@id="item_link"]').send_keys('https://nashpir.ru/product-category/sdobnye-pirogi/')
        #     self.driver.find_element(By.XPATH, '//*[@id="item_price"]').send_keys(int(k[3][:-1]))
        #     self.driver.find_element(By.XPATH, '//*[@id="item_weight"]').send_keys((k[2][:-1]))
        #     time.sleep(2)
        #     self.driver.find_element(By.XPATH, '//*[@id="market_ei_main_photo_upload"]/input').send_keys(k[1])
        #     time.sleep(2)
        #     self.driver.find_element(By.XPATH, '//*[@id="market_photo_crop_done"]').click()
        #     time.sleep(2)
        #     self.driver.find_element(By.XPATH, '//*[@id="box_layer"]/div[2]/div/div[3]/div[1]/div[1]/button[2]').click()
        #     time.sleep(2)
        #     self.driver.find_element(By.ID, 'market_add_item_btn').click()
        #     time.sleep(2)

        for i, k in data3.items():
            self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div[1]/div[1]/div/table/tbody/tr/td[1]/input[1]').send_keys('Еда на заказ')
            time.sleep(2)
            self.driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/ul/li').click()
            self.driver.find_element(By.XPATH, '//*[@id="item_name"]').send_keys(i)
            self.driver.find_element(By.XPATH, '//*[@id="item_sku"]').send_keys('Напиток')
            self.driver.find_element(By.XPATH, '//*[@id="item_description"]').send_keys(f'{i} напиток')
            self.driver.find_element(By.XPATH, '//*[@id="item_link"]').send_keys('https://nashpir.ru/product-category/napitki/')
            self.driver.find_element(By.XPATH, '//*[@id="item_price"]').send_keys(int(k[1][:-1]))
            # self.driver.find_element(By.XPATH, '//*[@id="item_weight"]').send_keys((k[2][:-1]))
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="market_ei_main_photo_upload"]/input').send_keys(k[0])
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="market_photo_crop_done"]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="box_layer"]/div[2]/div/div[3]/div[1]/div[1]/button[2]').click()
            time.sleep(2)
            self.driver.find_element(By.ID, 'market_add_item_btn').click()
            time.sleep(2)

    def deleting_goods(self):
        for i in range(68):
            self.driver.find_element(By.CLASS_NAME, 'market_row').click()
            time.sleep(1)
            self.driver.find_element(By.CLASS_NAME, 'ui_actions_menu_wrap _ui_menu_wrap market_item_menu_more').is_selected()
            self.driver.find_element(By.XPATH, '//*[@id="wk_content"]/div/div[2]/div/div[1]/div/div/div/div[3]/div[2]/a[3]').click()
            self.driver.find_element(By.XPATH, '//*[@id="wk_right"]/div').click()
            time.sleep(1)


# GetContentFromSite(requests_url4)

VkBot(requests_url3)





