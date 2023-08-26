from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
import time

chromedriver_path = 'C:\Addons\chromedriver\chromedriver.exe'

def solve_recaptcha(driver):
    # Očekujemo da se reCAPTCHA učita
    recaptcha_frame = driver.find_element(By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha']")
    driver.switch_to.frame(recaptcha_frame)
    
    # Pauza dok ručno rešavate reCAPTCHA
    input("Molim vas da ručno rešite reCAPTCHA i pritisnite Enter kada završite...")
    
    # Nakon što se reCAPTCHA ručno reši, prebacujemo se nazad na glavni okvir
    driver.switch_to.default_content()

    
def get_company_data(maticni_broj):
    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)
    driver.get('https://fin.apr.gov.rs/JavnaPretraga/Home/Index/')
    
    try:
        maticni_broj_input = driver.find_element(By.ID, 'RegNoModel_UserInput')
        maticni_broj_input.send_keys(maticni_broj)
        
        # Rešavanje reCAPTCHA
        solve_recaptcha(driver)
        
        pretrazi_dugme = driver.find_element(By.XPATH, '//button[contains(@class, "btn-default") and contains(text(), "Претрага")]')
        pretrazi_dugme.click()

        
        # Očekivanje da se prikažu rezultati pretrage
        wait = WebDriverWait(driver, 120)  # Ovde možete prilagoditi vreme čekanja
        wait.until(EC.presence_of_element_located((By.ID, 'result_table')))
        
        naziv = driver.find_element(By.XPATH, '//td[contains(text(), "Naziv")]//following-sibling::td').text
        broj_zaposlenih = driver.find_element(By.XPATH, '//td[contains(text(), "Broj zap")]//following-sibling::td').text
        delatnost = driver.find_element(By.XPATH, '//td[contains(text(), "Delatnost")]//following-sibling::td').text
        
        return {
            'Naziv kompanije': naziv,
            'Broj zaposlenih': broj_zaposlenih,
            'Delatnost kompanije': delatnost
        }
    finally:
        driver.quit()

maticni_broj = '20059966'
podaci = get_company_data(maticni_broj)

if podaci:
    print('Podaci o kompaniji:')
    for key, value in podaci.items():
        print(f'{key}: {value}')
else:
    print('Kompanija sa datim matičnim brojem nije pronađena.')

# Sačekajte unos Enter komande kako bi program nastavio sa izvršavanjem
input("Pritisnite Enter da zatvorite program...")