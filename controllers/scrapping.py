from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def get_video_list(query: str):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")  
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(f"https://www.freecodecamp.org/news/search/?query={query}")
        time.sleep(5)
        
        video_list = []
        post_cards = driver.find_elements(By.CLASS_NAME, "post-card")
        # print(post_cards)
        for card in post_cards:
            try:
                img = card.find_element(By.TAG_NAME, 'img')
                image_url = img.get_attribute('src')
            except:
                image_url = "No image found"
            try:
                title = card.find_element(By.TAG_NAME, 'h2').text
            except:
                title = "No title found"
            try:
                video = card.find_element(By.CLASS_NAME, 'post-card-image-link')
                video_url = video.get_attribute('href')
            except:
                video_url = "No video-link found"
            video_list.append({
                'title':title,
                'image_url':image_url,
                'video_url':video_url
            })
            
        driver.quit()
        return video_list
    except Exception as e:
        return e


# result = get_video_list("Machine learning")
# with open("./data/resources.json", 'w') as f:
#     f.write(json.dumps(result))