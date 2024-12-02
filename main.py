from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configurer le WebDriver pour Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Ouvrir le site Pages Jaunes
driver.get("https://www.pagesjaunes.fr/")
time.sleep(8)

# Gérer le popup de consentement aux cookies
try:
    cookies_skip = driver.find_element(By.ID, "didomi-notice-agree-button")
    cookies_skip.click()
except Exception as e:
    print(f"Aucun popup de consentement : {e}")

time.sleep(8)

# Effectuer la recherche
try:
    input_field = driver.find_element(By.ID, "quoiqui")
    input_field.send_keys("centre appel")

    input_ville = driver.find_element(By.ID, "ou")
    input_ville.send_keys("paris")

    search_res = driver.find_element(By.CLASS_NAME, 'icon-search')
    search_res.click()
    time.sleep(10)

    results = []
    items = driver.find_elements(By.CLASS_NAME, "bi-generic")
    
    for item in items:
        try:
            name = item.find_element(By.CLASS_NAME, "bi-activity-unit").text
        except:
            name = "N/A"

        try:
            # Récupérer les horaires
            hours = item.find_element(By.CLASS_NAME, "bi-activity-hours").text
        except:
            hours = "N/A"

        try:
            # Récupérer l'adresse
            address = item.find_element(By.CLASS_NAME, "bi-address").text
        except:
            address = "N/A"

        try:
        # Récupérer le téléphone en utilisant un sélecteur CSS
            phone = item.find_element(By.CLASS_NAME, "coord-numero noTrad selectorgadget_selected").text
        except:
            phone = "N/A"


        results.append({
            "Nom": name,
            "Adresse": address,
            "Téléphone": phone,
            "Horaires": hours
        })

    # Exporter les résultats dans un fichier Excel
    df = pd.DataFrame(results)
    df.to_excel("resultats_pages_jaunes.xlsx", index=False)
    print("Données exportées dans 'resultats_pages_jaunes.xlsx'")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")

input("Appuyez sur Entrée pour fermer le navigateur...")
driver.quit()
