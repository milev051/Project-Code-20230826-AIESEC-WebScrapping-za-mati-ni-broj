from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def main():
    # Inicijalizacija drajvera
    driver = webdriver.Chrome()
    
    # Otvori stranicu
    driver.get("https://fin.apr.gov.rs/JavnaPretraga/Home/Index/")
    
    # Unesi maticni broj
    maticni_broj = input("Unesite matični broj: ")
    maticni_input = driver.find_element(By.ID, "RegNoModel_UserInput")
    maticni_input.send_keys(maticni_broj)
    
    # Sacekaj korisnika da ručno reši reCAPTCHA
    input("Molimo vas da ručno rešite reCAPTCHA. Pritisnite Enter kada završite...")
    
    # Zatvori drajver
    driver.quit()

if __name__ == "__main__":
    main()
