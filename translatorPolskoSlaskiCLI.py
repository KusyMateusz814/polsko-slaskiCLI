from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os 
import sys 
import argparse

#parser = argparse.ArgumentParser()
## example jak to powinno wygladac @down
##parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
#args = parser.parse_args()

def def_environment():
     path_to_dir = os.path.dirname(os.path.realpath(__file__))
     #print("Scieszka do folderu:"+path_to_dir)
     os.environ["PATH"] += os.pathsep + path_to_dir

def change_polish_letter(language):
    return language.replace('ą','a').replace('ś','s')

def create_url(lang_from, lang_to):
    lang_from = change_polish_letter(lang_from)
    lang_to = change_polish_letter(lang_to)
    if(lang_from == "polski" and lang_to == "slaski"):
        return "https://silling.org/translator/?dir=pol-szl#translation"
    elif(lang_from == "slaski" and lang_to == "polski"):
        return "https://silling.org/translator/?dir=szl-pol#translation"
    else:
        print("wyglada na to ze podales zle jezyki - sprobuj jeszcze raz")
        exit()

def def_translator_polsko_slaski(lang_from, lang_to, sentence):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    end_url = create_url(lang_from, lang_to)
    driver.get(end_url)
    oznaczbtn = driver.find_element_by_xpath('//*[@id="markUnknown"]')
    driver.execute_script("arguments[0].click();", oznaczbtn)
    #input text to input filed translator 
    driver.find_element_by_xpath('//*[@id="originalText"]').send_keys(sentence)
    driver.find_element_by_xpath('//*[@id="translate"]').click()
    #UWAGa - kiedy zajrzysz inspectorem w ta strone, w textArea nie znajdziesz przetlumaczonego textu - wynika to z faktu ze on siedzi poza drzewem DOM, dlatego też potrzebne jest wywolanie na tym metody get_attribute('value')
    finishText = driver.find_element_by_xpath('//*[@id="translatedText"]').get_attribute('value')
    print(sentence+'\n-------')
    print(finishText)
    #do testow - bardzo przdatne
    #driver.save_screenshot('SlaskiTranslator.png')
    driver.quit()

def main():
    if len(sys.argv) > 3:
        lang_from = str(sys.argv[1])
        lang_to = str(sys.argv[2])
        sentence = str(sys.argv[3])
        def_translator_polsko_slaski(lang_from, lang_to, sentence)
    else:
        print("Coś nie tak z liczba argumentow, sprawdz liste argumentow skryptu")

if __name__ == "__main__":
    def_environment()
    main()


