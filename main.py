# Import required modules
import datetime
from datetime import date
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Define global variables for two rooms
global room390, room392
room390 = 'https://booking.sjlibrary.org/space/9736'
room392 = 'https://booking.sjlibrary.org/space/9737'

# Defines the driver to be used: Provides the google Chrome driver
def Chrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path='C:\\Users\\Freew\\OneDrive\\Desktop\\Python Projects\\chromedriver.exe', options=options)
    return driver

# Defines the driver to be used: Provides the fireFox driver
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
    
    # Initilization of getting the URL
    time.sleep(.5)
    driver.get(URL)
    
    # Set the size of the widow and it's position
    driver.set_window_size(1000, 1000)
    driver.set_window_position(0,0)
    
    # Creates loop to go through the days to go to the provided days in advance
    counter1 = 0
    while (counter1 < daysAdvance):
        # Clicks the next button
        nextButton = WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-next-button')))
        nextButton.click()
        counter1 = counter1 + 1
    
    # Identifies all the boxes that are present, both available and not available
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-timeline-event-harness')))
    timeboxloc_Parent = driver.find_elements(By.CLASS_NAME, parentTitle)
    
    # Counts through the boxes backwards in order to get the prime hours of the library
    backwardsBox = len(timeboxloc_Parent) - 1
    boxesClicked = 4
    while(boxesClicked > 0):
        # Reconizes if there are any boxes to click
        if(len(timeboxloc_Parent) == 0):
            driver.close()
            driver.quit()
            return 'full'
        # Clicks the green boxes
        else:
            greenbox = timeboxloc_Parent[backwardsBox].find_element(By.CLASS_NAME, timeboxloc_Child)
            WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable(greenbox)).click()
            boxesClicked = boxesClicked - 1
            backwardsBox = backwardsBox - 1
        
        # If no more boxes to click then stop clicking
        if(boxesClicked > len(timeboxloc_Parent) - 1):
            break
    
    # Click on the submit button and clear the unneccissary variable
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.NAME, submitbuttonloc))).click()
    timeboxloc_Parent.clear()
    
    # Wait and itentify the submit button
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((By.ID, submitbuttonID)))
    submit = driver.find_element(By.ID, submitbuttonID)
    
    # Locates the login boxes and separates them into two variables
    login = driver.find_elements(By.CLASS_NAME, logInfo)
    user = login[0]
    pw = login[1]
    
    # Sends the username and password from file to the web browser
    user.send_keys(Username)
    pw.send_keys(Password)
    
    # Clicks the submit buttion
    submit.click()
    
    # Initilizes a test sequence to identify if the page was left and cradentials were correct
    time.sleep(.5)
    try:
       driver.find_element(By.ID, contbuttonID)
       success = True
    except Exception:
        success = False
        pass
    
    if(success == False):
        time.sleep(.5)
        driver.close()
        print('invalid cradentials')
        return 'invalid cradentials'
    
    # Clicks the continue button
    cont = driver.find_element(By.ID, contbuttonID)
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable(cont)).click()
    
    # Clicks the done button
    done = driver.find_element(By.ID, submitbooking)
    WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable(done))
    
    # Sends a group name to the required box
    groupName = driver.find_element(By.ID, groupNameID)
    groupName.send_keys('IEEE Mentor Session')
    
    # Clicks the done button
    done.click()
    
    # Initializes a wait sequence to identify if any errors have occured
    time.sleep(.5)
    try:
       driver.find_element(By.ID, 's-lc-eq-success-buttons')
       success = True
    except Exception:
        success = False
        pass
    
    if(success == True):
        time.sleep(.5)
        driver.close()
        print('Success')
        return 'success'
    
    elif(success == False):
        print('fail')
        return 'user fail'

def fileread(myFile):
    # Opens file and reads
    file = open(myFile, "r")
    
    # Initializes lists to fill
    Username = []
    Password = []
    
    # Goes through each line and appends the values to Username and Password: File format (xxxxxx; xxxxxx)
    while(line := file.readline().rstrip()):
        users = line.split("; ", 1)
        
        Username.append(users[0])
        Password.append(users[1])
        
    return Username, Password

def main():
    # Calls to fileread to pull usernames and passwords off the provided file
    Username, Password = fileread("C:\\Users\\Freew\\OneDrive\\Desktop\\Python Projects\\Library Login\\Usernames and Password")
     
    # A loop for checks and reruns for all the users
    counter = 0
    while (counter < len(Username)):
        # Selects driver and adds a small wait
        driver = fireFox()
        time.sleep(.5)
        
        # Runs the Login module with the room, selected driver, number of days to skip, username, and password
        results = Login(room390, driver, 4, Username[counter], Password[counter])
        driver.quit()
        
        # Depending on which results were passed from Login() these decissions will be made
        # If success returns then try the next user
        if (results == 'success'):
            print('Successful run:', counter + 1)
            counter = counter + 1
        
        # If full returns then there's no rooms available on that day so no more runs required
        if (results == 'full'):
            print('No More Rooms Available')
            break
        
        # If user fail then there was an error with the number of times the user has booked so try the next
        if (results == 'user fail'):
            print('This user was already used')
            print('Trying Again...')
            counter = counter + 1
        
        # If invalid cradentials then the user's information wasn't accurate according to the library so return that user's 
        # inforamtion to an error log to be removed from code or modified to be correct
        if (results == 'invalid cradentials'):
            print('This user has the wrong information')
            
            file = open('fialLog.txt', 'w')
            text = str('User has failed ID: ' + Username[counter] + ' Password: ' + Password[counter])
            file.write(text)
            file.close()
            
            print('Trying Next...')
            counter = counter + 1
        
        # If none of the above cases occured then something unforseen has happend and just try again
        if (results != 'full' and results != 'success' and results != 'user fail' and results != 'invalid cradentials'):
            print('Error Occured')
            print('Trying Again...')

main()