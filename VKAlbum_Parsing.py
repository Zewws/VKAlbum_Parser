print('Загрузка...')

class PicAlbum:
    def __init__(self, title: str):
        self.title = title
        self.links = []
        self.size = 0
        
    def add_link(self, link:str):
        self.links.append(link)
        self.size += 1

    
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import requests, os

options = Options()
options.add_argument("--headless")
    
service = Service(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

def main():
    ipt = input('Для справки напишите help\nurl:\t')
    s = ipt.split()
    if len(s)>0 and len(s)<3:
        path = s[0]
        mode = s[1] if len(s)==2 else '-li'
        if path =='help':
            myhelp()
        elif path.find('vk.com/album')>-1: 
            if path.find('vk.com/album')<8:
                path = 'https://'+path[path.find('vk.com/album'):]
            
            try:
                albom = driverwork(path)
                print('Обработка '+str(albom.size)+' картинок')
                saving(albom, mode)
                print('Готово\n')
            except Exception as e:
                print(e)
                input()
            
        else:
            print('Нет такой команды. Введите help для справки')
    else:
        print('Убедитесь, что формат отправленой вами строки составленым по правилам из раздела help.')
        

def myhelp():
    print('Данная программа позволяет скачать картинки из альбомов ВК в папку с названием альбома, созданную рядом с файлом с программой.')
    print('Введите url альбома из вк\n(url обязательно должен содержать vk.com/album)\nи через пробел режим\nПо умолчанию: -li\tкартинки и ссылки в отдельной папке с названием альбома\n-l\tтолько ссылки\n-i\tтолько картинки')
    
def driverwork(path):
    driver.get(path)
    alb_title = driver.find_element('xpath', '/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/h1').text
    albom = PicAlbum(alb_title)
    print('Название: '+alb_title)
    el = driver.find_element(By.CLASS_NAME, 'photos_row')
    el.click()
    el_path = '/html/body/div[7]/div/div[2]/div/div[2]/div/div/button'
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, el_path)))
    el_path ='/html/body/div[7]/div/div[2]/div/div[2]/div/div/button'
    el = driver.find_element(By.XPATH, el_path)
    el.click()
    el_path = '/html/body/div[5]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/span'
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, el_path)))
    el = driver.find_element(By.XPATH, el_path)
    amount = int(el.text[5:])
    print('Картинок в альбоме: '+str(amount)+'\nПодождите.')
    el_path='//*[@id="pv_photo"]'
    el = driver.find_element(By.XPATH, el_path)
    try:
        for i in range(1, amount):
            pic = driver.find_element(By.XPATH, el_path+'/img')
            albom.add_link(pic.get_attribute('src'))
            el.click()
        pic = driver.find_element(By.XPATH, el_path+'/img')
        albom.add_link(pic.get_attribute('src'))
    except TypeError as e:
        print(pic.get_attribute('src'))
        print(type(pic.get_attribute('src')))
        raise e
    driver.quit()
    return albom


def saving(albom, mode='-li'):
    dr = 'albums\\'+albom.title+'\\'
    if not os.path.exists(dr):
        os.mkdir(dr)
    if 'l' in mode:
        if not os.path.exists(dr+'links.txt'):
            with open(dr+'links.txt', 'w') as w:
                w.write('')
    j=1
    for i in albom.links:
        if 'l' in mode:
            with open(dr+'links.txt', 'a') as a:
                a.write(i+'\n')
        if 'i' in mode:
            res = requests.get(i).content
            with open(dr+str(j)+'.jpg', 'wb') as output_file:
                output_file.write(res)
        j+=1
        
while True:
    if not os.path.exists('albums\\'):
        os.mkdir('albums\\')
    main()