"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import datetime
import math
import googlemaps
import twilio.rest

import tkinter as tk
import xml.etree.ElementTree as Et

from tkinter import *
from win32api import GetSystemMetrics
from classes.CardMachine import CardMachine
from classes.Mechanic import Mechanic
from classes.Notification import Notification
from classes.PopulateDataLists import PopulateDataLists
from pages.CardMachineOverviewPage import CardMachineOverviewPage
from pages.MechanicOverviewPage import MechanicOverviewPage
from pages.NotificationPage import NotificationPage
from pages.StartPage import StartPage


class NSDefectOverview(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self)

        # Initialise variables
        self.frames = {}

        self.buttonWidth = 110,
        self.buttonHeight = 70
        self.buttonBackgroundColor = "#212b5c"
        self.buttonForegroundColor = "#ffffff"
        self.buttonRelief = FLAT

        # 2:3 aspect ratio
        self.width = 800
        self.height = 533

        self.mechanicFile = "mechanics.xml"
        self.notificationFile = "notifications.xml"

        self.notification_information = []
        self.popup = None

        self.ns_api_username = "floris.dekruijff@student.hu.nl"
        self.ns_api_password = "FK7CDKplQPsyOpBuPtkURW8incvUdT3T2ZSVoSkrTRdF7r5ARvCOyQ"
        self.google_maps_api = googlemaps.Client(key='AIzaSyB3sE6Ekts-GoPlZ8vJ8P8i0UL1rVFnnPI')
        self.twilio_api = twilio.rest.Client("ACdf5a5cafa61b2fa3c98615176e80a6ac", "514dcdd9428ece0db966ec011a93a084")

        self.cardMachineList = PopulateDataLists.populate_card_machine_list(self.ns_api_username, self.ns_api_password)
        self.mechanicList = PopulateDataLists.populate_mechanic_list(self.mechanicFile)
        self.notificationList = PopulateDataLists.populate_notification_list(self.notificationFile)

        self.geometry("{}x{}+{}+{}".format(
            self.width,
            self.height,
            int(math.floor(GetSystemMetrics(0)) / 2 - self.width / 2),
            int(math.floor(GetSystemMetrics(1)) / 2 - self.height / 2) - 100)
        )

        self.title("NS Defect Overview")
        self.resizable(0, 0)

        # Initialise TkInter container settings.
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for page in (StartPage,
                     MechanicOverviewPage,
                     CardMachineOverviewPage,
                     NotificationPage):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.frames[StartPage] = StartPage(container, self)
        StartPage(container, self).grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == "NotificationPage":
            frame.update_notification_list()
        frame.tkraise()

    def write_notification(self, notification: Notification):
        tree = Et.parse(self.notificationFile)
        root = tree.getroot()
        notifications = Et.SubElement(Et.Element("notifications"), "notification")
        Et.SubElement(notifications, "time").text = notification.time
        Et.SubElement(notifications, "message").text = notification.message
        root.append(notifications)
        tree.write(self.notificationFile)

    @staticmethod
    def haversine_formula(latitude1, longitude1, latitude2, longitude2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        longitude1, latitude1, longitude2, latitude2 = map(math.radians, [longitude1, latitude1, longitude2, latitude2])
        # haversine formula
        delta_longitude = longitude2 - longitude1
        delta_latitude = latitude2 - latitude1
        a = math.sin(delta_latitude / 2) ** 2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(
            delta_longitude / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        d = 6367 * c
        return d

    def get_closest_mechanic(self, card_machine: CardMachine, exclude_mechanic: Mechanic):
        """
            This function loops through all the current mechanics and finds the one closest to the passed card machine
        """
        lowest = 0
        return_mechanic = None
        for mechanic in self.mechanicList:
            distance = NSDefectOverview.haversine_formula(
                float(card_machine.latitude), float(card_machine.longitude),
                float(mechanic.latitude), float(mechanic.longitude)
            )
            if lowest == 0:
                lowest = distance
            elif distance < lowest:
                lowest = distance
                if exclude_mechanic != mechanic:
                    return_mechanic = mechanic
        return lowest, return_mechanic

    def get_distance_travel_time(self, latitude1, longitude1, latitude2, longitude2):
        """
            This function calculates and returns the distance and travel time based on two coordinates
            @:return: distance, travel time
        """
        result = self.google_maps_api.distance_matrix((latitude1, longitude1), (latitude2, longitude2))
        return (result['rows'][0]['elements'][0]['distance']['text'].split(' ')[0],
                result['rows'][0]['elements'][0]['duration']['text'].split(' ')[0])

    def new_popup(self, title: str, message: str, buttons: list, popup_width: int, popup_height: int,
                  background_color: str):
        """
            This function creates a pop-up based on the passed parameters. It also generates buttons based on the passed
            list.
        """
        self.popup = tk.Tk()
        self.popup.wm_title(title)
        self.popup.geometry("{}x{}+{}+{}".format(
            popup_width,
            popup_height,
            int(self.winfo_x() + (self.width / 2 - popup_width / 2)),
            int(self.winfo_y() + (self.height / 2 - popup_height / 2))
        ))
        self.popup.configure(background=background_color)
        label = tk.Label(self.popup, text=message, background=background_color)
        label.pack(side="top", fill="x", pady=20, padx=20)

        if len(buttons) == 1:
            relative_x = 0.5
        else:
            relative_x = 1 / len(buttons) - 0.15

        rel_width = 80 / popup_width
        rel_height = 35 / popup_height
        for x in buttons:
            b = tk.Button(self.popup,
                          background=self.buttonBackgroundColor,
                          foreground=self.buttonForegroundColor,
                          relief=self.buttonRelief,
                          text=x['text'],
                          command=eval(x['command']))
            b.place(relwidth=rel_width, relheight=rel_height, relx=relative_x - (rel_width / 2), rely=0.45)
            relative_x += 0.3
        self.popup.mainloop()

    def new_notification(self):
        self.send_sms(self.notification_information[0], self.notification_information[1].phone_number)
        self.notification_information[1].set_attribute("availability", "Occupied", self.mechanicFile)
        self.notificationList.append(Notification(datetime.datetime.now(), self.notification_information[0]))
        self.popup.destroy()
        self.write_notification(self.notificationList[-1])

    def dispatch_mechanic(self, card_machine: CardMachine, mechanic: Mechanic):
        """
            This function dispatches a mechanic to a card machine, and updates the logs for it.
            It will update the Notification center as well.
        """
        message = ""
        title = ""
        buttons = []
        next_mechanic = self.get_closest_mechanic(card_machine, mechanic)

        travel_time = self.get_distance_travel_time(
            card_machine.latitude,
            card_machine.longitude,
            mechanic.latitude,
            mechanic.longitude)[1]

        self.notification_information = [
            "{mechanic_name} was dispatched to {station_name}, travel time is {travel_time} minutes.".format(
                mechanic_name=mechanic.name,
                station_name=card_machine.station_name,
                travel_time=travel_time),
            mechanic, card_machine
        ]

        if card_machine.defect == "Defect" and mechanic.availability == "Available":
            # Go directly to the create new event form.
            title = "Success"

            message = "{mechanic_name} has successfully been deployed to {station_name}".format(
                mechanic_name=mechanic.name,
                station_name=card_machine.station_name
            )

            buttons = [{"text": "Ok", "command": "self.new_notification"}]
            self.new_notification()

        elif card_machine.defect == "Defect" or card_machine.defect == "Operational" and mechanic.availability == "Occupied":
            title = "Are you sure?"

            message = "{station_name} is {station_status}, and the closest mechanic is occupied. \n " \
                      "The next is {mechanic_name} and is {distance} away, would you like to dispatch?".format(
                station_name=card_machine.station_name,
                station_status=card_machine.defect,
                mechanic_name=next_mechanic[1].name,
                distance=math.floor(next_mechanic[0])
            )

            buttons = [
                {"text": "Yes, I'm sure", "command": "self.new_notification"},
                {"text": "Cancel", "command": "self.popup.destroy"}
            ]

            self.notification_information[1] = next_mechanic[1]
            self.notification_information[0] = \
                "{mechanic_name} was dispatched to {station_name}, travel time is {travel_time} minutes.".format(
                    mechanic_name=next_mechanic[1].name,
                    station_name=card_machine.station_name,
                    travel_time=travel_time
                )

        elif card_machine.defect == "Operational" and mechanic.availability == "Available":
            title = "Are you sure?"

            message = "{station_name} is {station_status} and {mechanic_name} is {mechanic_status}".format(
                station_name=card_machine.station_name,
                station_status=card_machine.defect,
                mechanic_name=mechanic.name,
                mechanic_status=mechanic.availability.lower()
            )

            buttons = [
                {"text": "Yes, I'm sure", "command": "self.new_notification"},
                {"text": "Cancel", "command": "self.popup.destroy"}
            ]

        self.new_popup(title, message, buttons, 450, 125, "#fcc63f")

    def send_sms(self, message, number):
        try:
            pass
            # self.twilio_api.messages.create(
            #     to=number,
            #     from_="+3197014200218",
            #     body=message
            # )
        except twilio.base.exceptions.TwilioRestException:
            print("Number not accepted")
