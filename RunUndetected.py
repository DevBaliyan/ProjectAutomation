import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
import ctypes


import json

#<>Gemini ModUle
##for model in genai.list_models():
##    print(model.name)
from PIL import ImageGrab
import keyboard as kybd
from pynput.mouse import Controller
mouse = Controller()
import google.generativeai as genai
genai.configure(api_key=APIKEY)
x1, x2, x3, x4, scale = 0, 0, 0, 0, 2
job = ("Output should be strictly least character/characters possible out of 1,2,3,4,5 or combination in case mutiple are true, and 0 if not possibe to answer."
        " Return correct option as integer/integers without any separater. For example second and fourth option are correct, then return: 24."
        " Do not add any additional text except the rank of correct options. Options are listed 1-n increasing top to bottom in case they are not numbered and are in different lines. "
        "In case multiple options share single line then they are numbered incresing left to right then next line.\n\n\nQUESTION:\n")



def set_coord1():
    global x1, y1
    x1, y1 = mouse.position
    ctypes.windll.user32.MessageBeep(0)


def set_coord2():
    global x2, y2
    x2, y2 = mouse.position
    ctypes.windll.user32.MessageBeep(0)


def MCQ():
    print("MCQ")
    set_coord2()
    try:
        img = ImageGrab.grab(bbox=(x1*scale, y1*scale, x2*scale, y2*scale)).save("test.png")
        #img_bytes = BytesIO()
        #img.save(img_bytes, format='PNG')
        #img_bytes.seek(0)
        myfile = genai.upload_file("test.png")
        model_name = "gemini-2.0-flash" ##"gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        result = model.generate_content(
        [myfile, "\n\n", ("Output should be strictly 1 character out of 1,2,3,4 or more, and 0 if not possibe to answer. Analyze "
                          "the provided image containing a multiple-choice question (MCQ). The image has the question text and its "
                          "possible answers displayed. Return correct option as an integer. Do not add any additional text except the "
                          "rank of correct option 1-4 increasing top to bottom.")]
        )
        reply = result.text[0]
        print(result)
        try:
            driver.find_element(By.XPATH, f'//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/mcq-question/div/div[2]/div[2]/div/label/span').click()
            mouse.position = 1150, 75+250*(int(reply)-1)
        except:
            pass
        ctypes.windll.user32.MessageBeep(0)
    except:
        ctypes.windll.user32.MessageBeep(0)
        sleep(1)
        ctypes.windll.user32.MessageBeep(0)


def MCQ_():
    print("MCQ_")
    try:
        di = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/div[3]/h4').text
        t1 = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/mcq-question/div/div[1]/span/mathjax-renderer/div').text
        t2 = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/mcq-question/div/div[2]').text
        ques = di+'\n'+t1+'\nOptions: \n'+t2
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        reply = model.generate_content(f"{job} {ques}")
        reply = reply.text[0]
        driver.find_element(By.XPATH, f'//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/mcq-question/div/div[2]/div[{reply}]/div/label/span').click()
        ctypes.windll.user32.MessageBeep(0)
    except Exception as e:
        reply = str(e)
        ctypes.windll.user32.MessageBeep(-1)  # Different sound for errors
        sleep(0.5)
        ctypes.windll.user32.MessageBeep(-1)


#OVER

def AQGemini():
    ques = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/mcq-question/div/div[1]/span/mathjax-renderer/div').text
    opts = [element.text for element in driver.find_elements(By.XPATH, '//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/mcq-question/div/div[2]/div')]
    
            




def OpenTest():
    """Initial Step"""
    #From Main Page Of Test
    test_title = driver.find_element(By.CLASS_NAME, 'title').text




































def WaitForElementLinkText(link_text, wait_time=100, pause=0.5):
    global step
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
            )
        sleep(pause)
        element.click()
        step = 2
        return 1
    except TimeoutException:
        print("Element was not found within the specified time.")
        return 0


def WaitForElementXPATH(element_xpath, wait_time=100, pause=0.5):
    global step
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
            )
        sleep(pause)
        element.click()
        step = 2
        return 1
    except TimeoutException:
        print("Element was not found within the specified time.")
        return 0

    
def WaitForElementCSS(element_xpath, wait_time=60, pause=0.5):
    global step
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_xpath))
            )
        sleep(pause)
        element.click()
        return 1
    except TimeoutException:
        print("Element was not found within the specified time.")
        return 0


def handle_alert():
    ##global step
    try:
        WebDriverWait(driver, 25).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()  # To accept the alert (click "Reload")
        # alert.dismiss()  # To dismiss the alert (click "Cancel")
        return 1
    except TimeoutException:     
        print("No alert found.")
        driver.refresh()
        sleep(7)
        handle_alert()
        return 0


    
# Initialize the undetected ChromeDriver
options = uc.ChromeOptions()
options.add_argument("--start-maximized")  # Open browser in maximized mode
#options.add_argument(r"--disable-extensions-except=D:/Python/Project1/AlwaysActiveWindow.crx")
#options.add_argument(r"--load-extension=D:/Python/Project1/AlwaysActiveWindow.crx")
options.add_argument("--disable-popup-blocking")  # Disable popups
##options.add_argument("--remote-debugging-port=9222")  #Reconnect
options.add_argument(r"--user-data-dir=C:/DevExp")

# Reattach to the existing browser
driver = uc.Chrome(options=options)
driver.get("about:blank")  # Should now work

# Start the browser

try:
    # Open the desired URL
    driver.get("https://lpu.myperfectice.com/?logout=true")
    print("Website opened successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser after use
    #driver.quit()
    pass



#start   START
def Login():
    driver.find_element(By.NAME, "email").click()
    driver.find_element(By.NAME, "email").send_keys("12219980")
    driver.find_element(By.ID, "passInput").send_keys("LPU@31626")
    driver.find_element(By.ID, "passInput").send_keys(Keys.ENTER)


def Open_Test():
    WaitForElementLinkText("Test Series")
    driver.get("https://lpu.myperfectice.com/student/testSeries/details/6631a06ad257145d2992f532")
    WaitForElementLinkText("Resume")
    sleep(2)
    WaitForElementCSS(".ml-auto > .btn")
    sleep(3)
    WaitForElementLinkText("Ready to start")
    sleep(3)


def AttemptQuestion():
    ques = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/p-student/app-take-test/div/div/section/div/div[1]/div[1]/div/mcq-question/div/div[1]/span/mathjax-renderer/div').text
    ans  = find_best_match(ques)['answer']
    options = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.row.mb-2')))
    option_texts = []
    for option in options:
        text_element = option.find_element(By.CSS_SELECTOR, '.mathjax-container p')
        option_texts.append(text_element.text)
    best_match_text, similarity = find_best_match_opt(option_texts, ans)
    if similarity >= 0.85:
        for option in options:
            text_element = option.find_element(By.CSS_SELECTOR, '.mathjax-container p')
            if text_element.text == best_match_text:
                # Click the checkbox
                checkbox = option.find_element(By.TAG_NAME, 'input')
                checkbox.click()
                print(f"Clicked: {best_match_text} with similarity {similarity:.2f}")
                break
    else:
        print("No sufficiently similar match found.")
        
print("\nTest Run"*5)
def main():
    kybd.add_hotkey('alt+m', MCQ)
    kybd.add_hotkey('ctrl+`', MCQ_)
    kybd.add_hotkey('alt+z', set_coord1)
    kybd.add_hotkey('alt+x', set_coord2)
    print('Waiting...')
    kybd.wait('alt+del')
