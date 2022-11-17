# Actions to execute according to every possible target

# Twilio library
from twilio.rest import Client

# LG Smart TV (WebOS) library
from pywebostv.connection import *
from pywebostv.controls import *
import time


def options_menu(option):

    # Logging in to Twilio Sandbox for WhatsApp
    sid = 'ACb48f85d60f016e22c3cccec01865905f'
    authToken = '731036dd0d3a8975698b15c58fa270ef'
    twilioClient = Client(sid, authToken)

    # Establishing connection with TV
    client = WebOSClient("192.168.5.115")
    client.connect()
    store = {'client_key': 'a188f8cdafc3f0de4f2964e13b588d8b'}

    for status in client.register(store):

        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")

        elif status == WebOSClient.REGISTERED:
            print("Registration successful: Connected with Smart-TV!")




    # Selecting option
    if option == "VEN" or option == "SYM1":

        message = twilioClient.messages.create(to='whatsapp:+573172562808',
                                         from_='whatsapp:+14155238886',
                                         body='OPTION 1: VEN was the Target! xD')

    elif option == "BRZ" or option == "SYM2":

        message = twilioClient.messages.create(to='whatsapp:+573172562808',
                                         from_='whatsapp:+14155238886',
                                         body='OPTION 2')

    elif option == "USA" or option == "SYM3":

        message = twilioClient.messages.create(to='whatsapp:+573172562808',
                                         from_='whatsapp:+14155238886',
                                         body='OPTION 3')

    elif option == "UK" or option == "SYM4":

        media1 = MediaControl(client)
        media1.volume_up()

    elif option == "IND" or option == "SYM5":

        tv_control1 = TvControl(client)
        tv_control1.channel_up()

    elif option == "FIN" or option == "SYM6":

        tv_control1 = TvControl(client)
        tv_control1.channel_down()

    elif option == "ITA" or option == "SYM7":

        app1 = ApplicationControl(client)
        apps = app1.list_apps()  # Returns a list of `Application` instances.

        # Launching Netflix:
        yt = [x for x in apps if "netflix" in x["title"].lower()][0]
        launch_info = app1.launch(yt)

    elif option == "COL" or option == "SYM8":

        app1 = ApplicationControl(client)
        apps = app1.list_apps()  # Returns a list of `Application` instances.

        # Launching normal TV:
        tv = [x for x in apps if "tv" in x["title"].lower()][0]
        launch_info = app1.launch(tv)

    else:

        message = twilioClient.messages.create(to='whatsapp:+573172562808',
                                         from_='whatsapp:+14155238886',
                                         body='Target not detected!')


    #End!
    return



