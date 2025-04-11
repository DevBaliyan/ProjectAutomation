import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
import ctypes
import re
import Data


with open("NetworkRequest.js", 'r') as file: interceptScript = file.read() #&Block tab switches
a = '''document.addEventListener("mouseleave", (event) => event.stopImmediatePropagation(), true);
document.addEventListener("mouseout", (event) => event.stopImmediatePropagation(), true);

Object.defineProperty(document, 'fullscreenElement', {
        get: function() { return true; }
    });
console.log(`Done`);'''


def check_for_intercepted_requests():
    try:
        requests = driver.execute_script("return window.getInterceptedRequests();")
        if requests and len(requests) > 0:
            print(f"\nFound {len(requests)} intercepted requests:")
            for i, req in enumerate(requests):
                print(f"Request {i+1}:")
                print(f"URL: {req['url']}")
                print(f"Method: {req['method']}")
                
                # Parse the data if it exists
                if req['data']:
                    try:
                        import json
                        data = json.loads(req['data'])
                        if 'question' in data and 'question' in data['question']:
                            question_id = data['question']['question']
                            print(f"Question ID: {question_id}")
                    except:
                        print(f"Raw data: {req['data'][:100]}...")  # Print first 100 chars
                
                print("---")
            
            # Clear the array to avoid showing the same requests again
            driver.execute_script("window.requestData = [];")
        
        return requests and len(requests) > 0
    except Exception as e:
        print(f"Error checking intercepted requests: {e}")
        return False


def UpdateFile(file, text, message=None):
    with open(file, 'a', encoding='utf-8') as file:
        file.write(text)
    if not message:
        return
    print(message, end='')
    



#class textOperation:
def normalize(text):
    return text.replace("  ", '').replace('\n', '')

def category(test):
    match = re.search(r'\[(.+)\] (.+)', test)
    return match.group(1)+" "+match.group(2)[:-2] if match else None

def extract_options(options):
    """
    Extracts options labeled A:, B:, etc., while preserving indexing.
    Handles empty options, removes extra spaces, and ensures correct formatting.
    """
    # Find all option labels
    pattern = r'([A-E]:)'
    matches = list(re.finditer(pattern, options))
    if not matches:
        return []
    
    # Extract options by processing each label and the text up to the next label or end
    result = []
    for i in range(len(matches)):
        label = matches[i].group(1)  # e.g., "A:"
        start = matches[i].end()     # Position after the label
        # End is the start of the next label or the end of the string
        end = matches[i + 1].start() if i + 1 < len(matches) else len(options)
        value = options[start:end].strip()  # Get and clean the value
        # Append label alone if value is empty, otherwise label + space + value
        option = value#label + (" " + value if value else "")
        result.append(option.replace('\n', '').replace("  ", ""))
    
    return result

def urlToID(url):
    res = re.search('assessments.+?id=(.*)', url).group(1)
    return res if res else None


   

class elementWait:
    def WaitForElement(driver, byMethod, locator, wait_time=100, pause=0.5, message="Element was not found within the specified time."):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((byMethod, locator))
                )
            sleep(pause)
            return element
        except TimeoutException:
            print(message)
            return 0



class Automate:
    def __init__(self, driver):
        self.driver = driver
        
    def login(self):#Change, user, pwd):
        elementWait.WaitForElement(self.driver, By.NAME, "email", 5)
        self.driver.find_element(By.NAME, "email").click()
        self.driver.find_element(By.NAME, "email").send_keys("12219980")
        self.driver.find_element(By.ID, "passInput").send_keys("LPU@31626")
        self.driver.find_element(By.ID, "passInput").send_keys(Keys.ENTER)

    def openTest(self):
        elementWait.WaitForElement(self.driver, By.LINK_TEXT, "Test Series").click()
        self.driver.get("https://lpu.myperfectice.com/student/testSeries/details/6631a06ad257145d2992f532")
        elementWait.WaitForElement(self.driver, By.LINK_TEXT, "Resume").click()
        sleep(2)
        elementWait.WaitForElement(self.driver, By.CSS_SELECTOR, ".ml-auto > .btn").click()
        sleep(3)
        elementWait.WaitForElement(self.driver, By.LINK_TEXT, "Ready to start").click()
        sleep(3)
        self.driver.execute(a) #???
        
    def fetchSummary(self, tid=None):
        while "?id=" not in self.driver.current_url:
            sleep(0.25)
        tid = urlToID(self.driver.current_url)
        if elementWait.WaitForElement(self.driver, By.LINK_TEXT, 'Show Answer', 5):
            for element in self.driver.find_elements(By.LINK_TEXT, 'Show Answer'):
                element.click()
        tn = self.driver.find_element(By.CLASS_NAME, 'main_title').text#test_name
        total, added = 0, 0
        for element in self.driver.find_elements(By.XPATH, '//*[@id="accordion_solution"]/accordion/div'):
            total += 1
            element.click()
            ques = elementWait.WaitForElement(self.driver, By.CLASS_NAME, 'qqq').text
            opts = [i.text for i in self.driver.find_elements(By.CSS_SELECTOR, '.p-0.pl-2')]
            ans = opts[ord(self.driver.find_element(By.CLASS_NAME, "green").text)-65]
            if dm.addQuestionFromSummary(ques+'a', opts, ans, tid, category(tn)):
                added += 1
            else:
                UpdateFile(f'{tn}.csv', f"{tid},'{ques}',{opts},{ans}\n")
            sleep(0.5)
        print(f'{added}/{total}')
            

    def attemptQues():
        ques = elementWait.WaitForElement(self.driver, By.CLASS_NAME, "question-item").text
        opts = [opt.text for opt in self.driver.find_elements(By.CLASS_NAME, 'answer-text')]
        btns = [btn.text for btn in self.driver.find_elements(By.CLASS_NAME, 'checkmark')]






options = uc.ChromeOptions()#.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
#options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_argument("--start-maximized")
options.add_argument("--disable-popup-blocking")
options.add_argument(r"--user-data-dir=D:\Python\ProjectAutomation\DevExp")#Error if directory is corrupt


# Reattach to the existing browser
driver = uc.Chrome(options=options)
print("Navigating to the test page...")
driver.get("https://lpu.myperfectice.com/student/assessments/%5BBeginner%20Learning%5D%20Reasoning%20-%20Symbols,%20Analogy%20and%20Coding-1?id=6634c4107e14581412fb5628")
driver.execute_script(interceptScript)
dm = Data.DataManager('temp.db')
a = Automate(driver)
a.login()
