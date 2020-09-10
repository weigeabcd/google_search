
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import requests
import re
import datetime
from fake_useragent import UserAgent

def save(filename, contents):
    fh = open(filename, 'a', encoding='utf-8')
    fh.write(contents)
    fh.close()

def re_finall_target_url(html):
    url_list = re.findall(r'<a href="(https://en.imsilkroad.com.*?)"', html)
    if url_list:
        return url_list
    else:
        return []

def render_txt_to_list(files):
    with open(files, "r") as f:
        data = f.readlines()
        # print(data)
        return data

def proxy_ip():
    # ip_url = "https://www.cloudam.cn/ip/takeip/5f2115d50bbfc4ec91b16c47?protocol=proxy&regionid=us&needpwd=false&duplicate=true&amount=1&type=text"
    ip_url = "https://www.cloudam.cn/ip/takeip/a5ETdYkhE4UdUaAFhyCTNQ0Trozn3OWe?protocol=proxy&regionid=us&needpwd=false&duplicate=true&amount=1&type=text"
    res = requests.get(ip_url)
    if res.status_code == 200:
        print(res.text)
        return res.text
    else:
        return ''

def get_random():
    return UserAgent().random

def google_search_by_keyword(keyword):
    chromeOptions = webdriver.ChromeOptions()
    # daili_ip="1"
    daili_ip = proxy_ip()
    chromeOptions.add_argument("--proxy-server=http://" + daili_ip)
    ua = get_random()
    chromeOptions.add_argument('User-Agent=' + ua)
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    try:
        browser.maximize_window()
        browser.implicitly_wait(10)
        browser.get("https://www.google.com/")
        wait = WebDriverWait(browser, 20)
        sleep(3)
        browser.find_element_by_class_name("gLFyf").send_keys(keyword)
        sleep(1)
        browser.find_element_by_class_name("gLFyf").send_keys(Keys.ENTER)

        # html = browser.page_source
        # print(html)
        find_status = False
        for i in range(10):
            # print("000")
            inpup_box = wait.until(EC.presence_of_element_located((By.ID, 'pnnext')))
            # print(inpup_box)
            if inpup_box:
                a_link_list = browser.find_elements_by_xpath('//div[@class="g"]/div/div[@class="r"]')
                # print(a_link_list)
                for a_link in a_link_list:
                    url = a_link.find_element_by_css_selector("a").get_attribute('href')
                    # print(url)
                    if "https://en.imsilkroad.com" in url:
                        print("存在", url)
                        find_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        a_link.find_element_by_css_selector("a").click()
                        sleep(3)
                        random_url_list = []
                        for j in range(3):
                            url_list = re_finall_target_url(browser.page_source)
                            random_url = url_list[random.randint(0, len(url_list))]
                            print("随机地址：", random_url)
                            browser.get(random_url)
                            start_time = random.randint(20,40)
                            sleep(start_time)
                            random_url_content = random_url+"-停留了："+str(start_time)+"秒"
                            random_url_list.append(random_url_content)

                        find_status = True
                        break
                if find_status:
                    # 记录下找到的信息内容
                    start_content = "，".join(random_url_list)
                    contents = find_time+" 使用代理："+daili_ip+"，搜索关键词："+keyword+" 在第"+str(i+1)+"页找到目标站点："+url+"。随机点击网站信息："+start_content+"\n"
                    save("info.txt", contents)
                    break
                else:
                    browser.find_element_by_id("pnnext").click()
                    sleep(1)
    except Exception as e:
        print(e,"1")
    browser.close()
    browser.quit()


def main():
    for i in range(10):
        keyword_list = render_txt_to_list("keywords.txt")
        for keyword in keyword_list:
            keyword = keyword.strip()
            google_search_by_keyword(keyword)


main()
