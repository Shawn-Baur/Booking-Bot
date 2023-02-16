import datetime
from datetime import date
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def Chrome():
    # driver = webdriver.Chrome(executable_path= 'C:\\Users\\Freew\\OneDrive\\Desktop\\Python Projects\\chromedriver.exe')
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path='C:\\Users\\Freew\\OneDrive\\Desktop\\Python Projects\\chromedriver.exe', options=options)
    return driver

def fireFox():
    driver = webdriver.Firefox(executable_path= 'C:\\Users\\Freew\\OneDrive\\Desktop\\Python Projects\\geckodriver.exe')
    return driver

def Login(URL, driver, daysAdvance, Username, Password):
    
    #Defined terms for the html locators and a wait value to provide as a max for the driver
    timeboxloc_Child = 'fc-event-main'
    parentTitle = 's-lc-eq-avail'
    submitbuttonloc = 'submit_times'
    submitbuttonID = 's-libapps-login-button'
    logInfo = 'form-control'
    contbuttonID = 'terms_accept'
    submitbooking = 's-lc-eq-bform-submit'
    groupNameID = 'nick'
    waitTime = 600
    
    time.sleep(.5)
    driver.get(URL)
    
    driver.set_window_size(1000, 1000)
    driver.set_window_position(0,0)
    
    counter1 = 0
    while (counter1 < daysAdvance):
        nextButton = WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-next-button')))
        nextButton.click()
        counter1 = counter1 + 1
    
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-next-button')))
    timeboxloc_Parent = driver.find_elements(By.CLASS_NAME, parentTitle)
    
    backwardsBox = len(timeboxloc_Parent) - 1
    boxesClicked = 4
    while(boxesClicked > 0):
        if(len(timeboxloc_Parent) == 0):
            driver.close()
            driver.quit()
            full = 'Full'
            return full
        
        greenbox = timeboxloc_Parent[backwardsBox].find_element(By.CLASS_NAME, timeboxloc_Child)
        WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable(greenbox)).click()
        boxesClicked = boxesClicked - 1
        backwardsBox = backwardsBox - 1
        
        if(boxesClicked > len(timeboxloc_Parent) - 1):
            break
    
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.NAME, submitbuttonloc))).click()
    timeboxloc_Parent.clear()
    
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.ID, submitbuttonID)))
    submit = driver.find_element(By.ID, submitbuttonID)
    
    login = driver.find_elements(By.CLASS_NAME, logInfo)
    user = login[0]
    pw = login[1]
    
    user.send_keys(Username)
    pw.send_keys(Password)
    
    submit.click()
    
    cont = driver.find_element(By.ID, contbuttonID)
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable(cont)).click()
    
    done = driver.find_element(By.ID, submitbooking)
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable(done))
    
    groupName = driver.find_element(By.ID, groupNameID)
    groupName.send_keys('IEEE Mentor Session')
    
    done.click()
    success = 'Success'
    time.sleep(.5)
    driver.close()
    return success

def fileread(myFile):
    file = open(myFile, "r")
    
    Username = []
    Password = []
    
    while(line := file.readline().rstrip()):
        users = line.split("; ", 1)
        
        Username.append(users[0])
        Password.append(users[1])
        
    return Username, Password

def main():
    Username, Password = fileread("C:\\Users\\Freew\\OneDrive\\Desktop\\Python Projects\\Library Login\\Usernames and Password")
     
    counter = 0
    while (counter < len(Username)):
        driver = fireFox()
        time.sleep(.5)
        
        results = Login('https://booking.sjlibrary.org/space/9736', driver, 4, Username[counter], Password[counter])
        driver.quit()
        print(results)
        
        if (results == 'Success'):
            print('Successful run:', counter + 1)
            counter = counter + 1
            
        if (results == 'Full'):
            print('No More Rooms Available')
            break
        
        if (results != 'Full' and results != 'Success'):
            print('Error Occured: Trying Again')
        

main()
