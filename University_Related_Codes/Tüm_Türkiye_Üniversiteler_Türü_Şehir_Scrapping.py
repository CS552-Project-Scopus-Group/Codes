from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from unidecode import unidecode

# Chrome seçeneklerini ayarlayın
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Chrome WebDriver başlatma
driver = webdriver.Chrome(options=options)

# URL'yi belirle
url = "https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp"

# Excel'e kaydedilecek veriler
data = []

# URL'yi açalım
driver.get(url)
time.sleep(3)  # Sayfanın yüklenmesi için bekleyin

try:
    # Tablo satırlarını bul
    table_xpath = "/html/body/div/div[2]/div/table/tbody/tr"
    rows = driver.find_elements(By.XPATH, table_xpath)
    total_rows = len(rows)  # Toplam satır sayısını al

    for i in range(1, total_rows + 1):  # Satırları işle
        try:
            # Üniversite ismi
            university_xpath = f'{table_xpath}[{i}]/td[1]/a'
            university_elem = driver.find_element(By.XPATH, university_xpath)
            university_name = university_elem.text.strip() if university_elem else "N/A"

            # Şehir bilgisi
            city_xpath = f'{table_xpath}[{i}]/td[2]'
            city_elem = driver.find_element(By.XPATH, city_xpath)
            city_name = city_elem.text.strip() if city_elem else "N/A"

            # Tür bilgisi
            type_xpath = f'{table_xpath}[{i}]/td[3]'
            type_elem = driver.find_element(By.XPATH, type_xpath)
            uni_type = type_elem.text.strip() if type_elem else "N/A"

            # İngilizce harflerle veriyi temizle
            university_name = unidecode(university_name)
            city_name = unidecode(city_name)
            uni_type = unidecode(uni_type)

            # Veriyi listeye ekle
            data.append([university_name, city_name, uni_type])

        except Exception as e:
            print(f"Error processing row {i}: {e}")
            continue

    print(f"Data successfully collected from {url}")

except Exception as e:
    print(f"Error extracting data from {url}: {e}")

# Veriyi DataFrame'e çevirme
df = pd.DataFrame(data, columns=["University", "City", "Type"])

# Excel dosyasına kaydetme
file_path = r"C:\Users\alibaki.turkoz\Desktop\university_list.xlsx"
df.to_excel(file_path, index=False)

# Tarayıcıyı kapat
driver.quit()

print(f"Data has been saved to {file_path}")
