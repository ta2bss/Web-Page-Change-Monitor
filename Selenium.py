from selenium import webdriver

option = webdriver.ChromeOptions()
"""option.add_argument('headless')"""


# chrome driver yükleme ve sayfaya gitme
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=option)
driver.get("https://nodes.guru/")



element = driver.find_element_by_id('id_of_an_element')
print(element.text)