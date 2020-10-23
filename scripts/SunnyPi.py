import time
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from selenium import webdriver
from pyvirtualdisplay import Display
from waveshare_epd import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont

try:

    print("Initializing Display")
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    refresh_image = Image.new('1', (epd.height, epd.width), 255) 
    refresh_draw = ImageDraw.Draw(refresh_image)

    loading_image = Image.new('1', (epd.height, epd.width), 255) 
    loading_draw = ImageDraw.Draw(loading_image)
    epd.displayPartBaseImage(epd.getbuffer(loading_image))    
    epd.init(epd.PART_UPDATE)

    font8 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 8)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)

    LOGINURL = "https://sunnyportal.com/Templates/Start.aspx"
    LOGOUTURL = "https://sunnyportal.com/Templates/Logout.aspx"

    loading_draw.text((0, 0), "Loading components...", font = font15, fill = 0)
    loading_draw.text((0, 20), "Please wait...", font = font15, fill = 0)
    loading_draw.text((0, 40), "This could take some time :)", font = font15, fill = 0)
    loading_image = loading_image.transpose(Image.ROTATE_180)
    epd.displayPartial(epd.getbuffer(loading_image))
    loading_image = loading_image.transpose(Image.ROTATE_180)

    print("Starting the Chromium Webdriver...")
    
    #Create a virtual display to 'show' the Chromium browser
    display = Display(visible=0, size=(800, 600))
    display.start()    
    driver = webdriver.Chrome('/usr/bin/chromedriver')

    while True: 

        #loading_draw = ImageDraw.Draw(loading_image)
        #loading_draw.text((0, 20), "Navigating to Login Page...", font = font15, fill = 0)
        #loading_image = loading_image.transpose(Image.ROTATE_180)
        #epd.displayPartial(epd.getbuffer(loading_image))
        #loading_image = loading_image.transpose(Image.ROTATE_180)

        print("Navigating to Login Page...")      
        driver.get(LOGINURL)
        email_element = driver.find_element_by_id("txtUserName")
        password_element = driver.find_element_by_id("txtPassword")
        checkbox_element = driver.find_element_by_id("ctl00_ContentPlaceHolder1_Logincontrol1_MemorizePassword")
        login_element = driver.find_element_by_id("ctl00_ContentPlaceHolder1_Logincontrol1_LoginBtn")

        #loading_draw = ImageDraw.Draw(loading_image)
        #loading_draw.text((0, 40), "Entering Login Credentials...", font = font15, fill = 0)
        #loading_image = loading_image.transpose(Image.ROTATE_180)
        #epd.displayPartial(epd.getbuffer(loading_image))
        #loading_image = loading_image.transpose(Image.ROTATE_180)

        print("Entering Login Credentials...")
        email_element.send_keys("youremail@address.com")
        password_element.send_keys("yourpassword")
        checkbox_element.click()

        #loading_draw = ImageDraw.Draw(loading_image)
        #loading_draw.text((0, 60), "Navigating to Dashboard...", font = font15, fill = 0)
        #loading_image = loading_image.transpose(Image.ROTATE_180)
        #epd.displayPartial(epd.getbuffer(loading_image))
        #loading_image = loading_image.transpose(Image.ROTATE_180)

        print("Navigating to Dashboard...")
        login_element.click()

        refreshcounter = 0
        relogincounter = 0
        keepActive = True

        #loading_draw = ImageDraw.Draw(loading_image)
        #loading_draw.text((0, 80), "Loading Dashboard...", font = font15, fill = 0)
        #loading_image = loading_image.transpose(Image.ROTATE_180)
        #epd.displayPartial(epd.getbuffer(loading_image))
        #loading_image = loading_image.transpose(Image.ROTATE_180)

        epd.init(epd.FULL_UPDATE)
        epd.display(epd.getbuffer(refresh_image))
        epd.init(epd.PART_UPDATE)

        time_image = Image.new('1', (epd.height, epd.width), 255) 
        time_draw = ImageDraw.Draw(time_image)
        epd.displayPartBaseImage(epd.getbuffer(time_image))    
        epd.init(epd.PART_UPDATE)
        bmpleaf = Image.open(os.path.join(picdir, 'leaf_small.bmp'))
        bmpsun = Image.open(os.path.join(picdir, 'sun_small.bmp'))
        bmpenergy = Image.open(os.path.join(picdir, 'energy_small.bmp'))
        time_image.paste(bmpleaf, (167, 41))
        time_image.paste(bmpsun, (0, 41))
        time_image.paste(bmpenergy, (84, 41))

        print("Loading Dashboard...")
        while keepActive:
            MainValues = driver.find_elements_by_class_name("mainValueAmount")
            MainValueUnits = driver.find_elements_by_class_name("mainValueUnit")
            Timestamps = driver.find_elements_by_class_name("widgetSubHead")
            MainValueDescriptions = driver.find_elements_by_class_name("mainValueDescription")

            TotalPVEnergy = driver.find_element_by_id('ctl00_ContentPlaceHolder1_UserControlShowDashboard1_energyYieldWidget_energyYieldTotalValue').text
            TotalPVEnergyUnit = driver.find_element_by_id('ctl00_ContentPlaceHolder1_UserControlShowDashboard1_energyYieldWidget_energyYieldTotalUnit').text
            TotalCO2 = driver.find_element_by_id('ctl00_ContentPlaceHolder1_UserControlShowDashboard1_carbonWidget_carbonReductionTotalValue').text
            TotalCO2Unit = driver.find_element_by_id('ctl00_ContentPlaceHolder1_UserControlShowDashboard1_carbonWidget_carbonReductionTotalUnit').text

            CurrentPVPowerValue = MainValues[0].text
            CurrentPVEnergyValue = MainValues[1].text
            CurrentCO2Avoided = MainValues[2].text

            CurrentPVPowerValueUnit = MainValueUnits[0].text
            CurrentPVEnergyValueUnit = MainValueUnits[1].text
            CurrentCO2AvoidedUnit = MainValueUnits[2].text

            CurrentPVEnergyDescription = MainValueDescriptions[0].text
            CurrentCO2Description = MainValueDescriptions[1].text

            CurrentTime = Timestamps[0].get_attribute("title")
            commasplit = CurrentTime.split(',')
            day = commasplit[0]
            date = (commasplit[1])[:-5]
            hour = commasplit[2]
            CurrentTimeFormatted = day+','+date+','+hour
            print ("Last updated: " + CurrentTimeFormatted)
            print("Current PV Power: " + CurrentPVPowerValue + CurrentPVPowerValueUnit)
            print("PV Energy: " + CurrentPVEnergyValue + CurrentPVEnergyValueUnit + " " + CurrentPVEnergyDescription + " (Total: " + TotalPVEnergy + TotalPVEnergyUnit + ")")
            print("CO2 Avoided: " + CurrentCO2Avoided + CurrentCO2AvoidedUnit + " " + CurrentCO2Description + " (Total: " + TotalCO2 + TotalCO2Unit + ")")
            print()

            if (CurrentPVEnergyDescription != 'Today'):
                CurrentPVEnergyDescription = 'Today'
                CurrentPVEnergyValue = '0'
            if (CurrentCO2Description != 'Today'):
                CurrentCO2Description = 'Today'
                CurrentCO2Avoided = '0'

            time_draw = ImageDraw.Draw(time_image)

            time_draw.rectangle([(0,0),(250,20)], fill = 255)
            time_draw.text((0, 0), CurrentTimeFormatted, font = font15, fill = 0)

            time_draw.rectangle([(23,42),(84,60)], fill = 255)
            time_draw.text((23, 42), CurrentPVPowerValue + CurrentPVPowerValueUnit, font = font15, fill = 0)
            time_draw.rectangle([(106,42),(167,60)], fill = 255)
            time_draw.text((106, 42), CurrentPVEnergyValue + CurrentPVEnergyValueUnit, font = font15, fill = 0)         
            time_draw.rectangle([(189,42),(250,60)], fill = 255)
            time_draw.text((189, 42), CurrentCO2Avoided + CurrentCO2AvoidedUnit, font = font15, fill = 0)

            time_draw.text((24, 60), "Current", font = font8, fill = 0)
            time_draw.text((108, 60), CurrentPVEnergyDescription, font = font8, fill = 0)
            time_draw.text((192, 60), CurrentCO2Description, font = font8, fill = 0)

            time_draw.rectangle([(110,80),(250,100)], fill = 255)
            time_draw.text((0, 80), "Total generated: " + TotalPVEnergy + TotalPVEnergyUnit, font = font15, fill = 0)
            time_draw.rectangle([(112,100),(250,120)], fill = 255)
            time_draw.text((0, 100), "Total CO2 saved: " + TotalCO2 + TotalCO2Unit, font =  font15, fill = 0)

            time_image = time_image.transpose(Image.ROTATE_180)
            epd.displayPartial(epd.getbuffer(time_image))
            time_image = time_image.transpose(Image.ROTATE_180)

            #Updating the page every 10 seconds.
            time.sleep(10)
            refreshcounter += 1
            relogincounter += 1

            #10 seconds x 360 loops = Re-login after 30 minutes.
            if (relogincounter == 180):
                print("Logoff")
                driver.get(LOGOUTURL)
                relogincounter = 0
                refreshcounter = 0
                keepActive = False
            #10 seconds x 60 loops = Refreshing the page after 10 minutes.
            if (refreshcounter == 60):
                print("Refreshing Page")
                driver.refresh()
                refreshcounter = 0


except KeyboardInterrupt:    
    print("Keyboard Interrupt. Clearing Screen...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd.sleep()
    epd.Dev_exit()
    os.system('pkill Xvfb')
    os.system('pkill chromedriver')
    os.system('pkill chromium-browse')
    exit()