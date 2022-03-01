import tkinter
from tkinter import *
from tkinter.ttk import *
from data import *
import datetime
from time import strftime
from tkinter import messagebox

GREY = "#D8D2CB"
DARK_BLUE = "#1C658C"
COLOR_ = "#398AB9"
d = Data()


class Screen:
    def __init__(self):
        global btn_clk
        btn_clk = False
        global station_list
        global temp_list_7
        global date_list
        global wd
        station_list = []
        temp_list_7 = []
        date_list = []
        wd = d.get_current_weather()
        self.no = 0
    def app(self, statii):
        global window
        window = Tk()
        window.title("MeteoRO")
        window.minsize(width=600, height=300)
        window.config(bg=DARK_BLUE)
        global canvas
        global temp_text
        global neb_text
        global clock_widget

        canvas = Canvas(window, width=600, height=280, bg=GREY, highlightthickness=0)
        current_state = canvas.create_text(135, 20, text="Starea actuala: ", font=("Times New Roman", 14, "normal"),
                                           fill="#1C658C")
        temp_text = canvas.create_text(300, 125, text="", fill=COLOR_, font=("Times New Roman", 36, "normal"))
        neb_text = canvas.create_text(110, 120, text="", fill=COLOR_, font=("Times New Roman", 50, "normal"))
        clock_widget = canvas.create_text(480, 125, text="", fill=COLOR_, font=("Times New Roman", 18, "normal"))
        canvas.grid(column=0, row=1, columnspan=2)

        label_select = tkinter.Label(window, text="Selectati o statie meteo: ", bg=DARK_BLUE, fg="white")

        label_select.grid(column=0, row=0)

        n = StringVar()
        n.set("Select")

        lista = Combobox(window, state="readonly", textvariable=n, width=27)
        lista.grid(column=1, row=0)
        lista['values'] = statii

        btn_img = PhotoImage(file="prog_btn_img.png")
        global prog_meteo_btn
        prog_meteo_btn = tkinter.Button(text="Prognoza Meteo", command=self.prog_window, image=btn_img,
                                        highlightthickness=0, relief="groove")
        prog_meteo_btn_window = canvas.create_window(300, 220, window=prog_meteo_btn)

        def statie_selectata(event):
            '''Gets hold of the selected station's name, appends it to a list, and updates the data on screen.'''
            global statie_selectata
            global station
            global crd
            global day_w
            statie_selectata = n.get()
            station = str(statie_selectata)
            station_list.append(station)
            self.update_cnv()
            # get_temp(station)
            crd = d.get_coord(station)
            day_w = self.get_weather()
            temp_list_7.clear()

        window.bind('<<ComboboxSelected>>', statie_selectata)

        window.mainloop()

    def update_cnv(self):
        '''Gets hold of the temperature and the cloud cover, and updates the values on the main canvas.'''
        canvas.itemconfig(temp_text, text=f"{self.get_temp(station)}°C")
        self.neb_img(self.get_neb(station))
        self.clock()

    def get_temp(self, station):
        '''Iterates through all of the entries (stations) provided by the Meteo Romania API, checks if any entry
        corresponds to the user input, returns the temperature for said location.'''
        global temperatura
        for i in range(len(wd["features"])):
            if wd["features"][i]["properties"]["nume"].title() == station:
                # print(f"Statia {station} exista")
                temperatura = wd["features"][i]["properties"]["tempe"]
                return temperatura

    def get_neb(self, station):
        '''Same functionality as get_temp, except for the cloud cover.'''
        for i in range(len(wd["features"])):
            if wd["features"][i]["properties"]["nume"].title() == station:
                # print(f"Statia {station} exista")
                neb = wd["features"][i]["properties"]["nebulozitate"]
                return neb

    def clock(self):
        '''Simple clock widget. Uses strftime to get hold of current time, calling itself every second in order to
         keep track of time.'''
        string = strftime("  %H:%M:%S\n%d/%m/%Y")
        window.after(1000, self.clock)
        canvas.itemconfig(clock_widget, text=string)

    def neb_img(self, neb):
        '''Takes input from get_neb, and depending on its value, changes it to an emoji according to the cloud cover.
        Eg: "cer acoperit" = ☁. Return only the emoji.'''
        if neb == "cer senin":
            canvas.itemconfig(neb_text, text="☀", font=("Times New Roman", 56, "normal"), fill="yellow")
        elif neb == "cer partial noros":
            canvas.itemconfig(neb_text, text="🌥", fill="grey", font=("Times New Roman", 56, "normal"))
        elif neb == "indisponibil":
            canvas.itemconfig(neb_text, text=" Date referitoare la nebulozitate\n    momentan indisponibile",
                              font=("Times New Roman", 12, "normal"), fill="red")
        elif neb == "cer acoperit":
            canvas.itemconfig(neb_text, text="☁", fill="grey", font=("Times New Roman", 56, "normal"))
        else:
            return neb

    def get_7days_temp(self):
        '''Gets hold of each day's temperature and converts it from K to C, adding each value to a list.
        Also, gets hold of current day and next 7 days date.'''

        for day in day_w["daily"]:
            temp = round(day["temp"]["day"] - 272.15)
            temp_f = f"{temp}°C"
            temp_list_7.append(temp_f)

        for i in range(7):
            today = datetime.date.today()
            next_day = today + datetime.timedelta(days=i)
            next_day_f = next_day.strftime("%d/%m")
            date_list.append(next_day_f)

    def create_prog_labels(self):
        '''Creates 7 labels, one for each day. Updates each label according to the date and weather condition. '''

        new0 = cnv_prog.create_text(40, 90, text=f"{date_list[1]}\n {temp_list_7[0]}", fill="grey",
                                    font=("Times New Roman", 16, "normal"))
        new1 = cnv_prog.create_text(110, 90, text=f"{date_list[2]}\n {temp_list_7[1]}", fill="grey",
                                    font=("Times New Roman", 16, "normal"))
        new2 = cnv_prog.create_text(180, 90, text=f"{date_list[3]}\n {temp_list_7[2]}", fill="grey",
                                    font=("Times New Roman", 16, "normal"))
        new3 = cnv_prog.create_text(250, 90, text=f"{date_list[4]}\n {temp_list_7[3]}", fill="grey",
                                    font=("Times New Roman", 16, "normal"))
        new4 = cnv_prog.create_text(320, 90, text=f"{date_list[5]}\n {temp_list_7[4]}", fill="grey",
                                    font=("Times New Roman", 16, "normal"))
        new5 = cnv_prog.create_text(390, 90, text=f"{date_list[6]}\n {temp_list_7[5]}", fill="grey",
                                    font=("Times New Roman", 16, "normal"))

    def prog_window(self):
        '''Opens the weather prognosis window when pressing the "Prognoza Meteo" button.
        Checks to see if any station was selected and calls the other functions responsible for creating the labels
        and updating them according to date and temperature.
        If no station was selected, a message box is shown, requesting the user to select a station.'''

        try:
            if btn_clk is False and station_list[-1] == station:
                global cnv_prog

                prog_win = Toplevel(window, width=500, height=300)
                prog_win.title("Prognoza")
                cnv_prog = Canvas(prog_win, width=500, height=300, bg=GREY)
                cnv_prog.grid(column=0, row=0)
                cnv_prog.create_text(250, 30, text="Prognoza pentru urmatoarele 7 zile")
                print(station_list)
                self.get_7days_temp()
                self.create_prog_labels()

        except IndexError:
            select_station = tkinter.messagebox.showwarning(title="Error", message="Please select a station first.")

    def get_weather(self):
        '''Calls the OpenWeatherMap API in order to get hold of the weather prognosis. Returns a dictionary containing
        the data.'''

        params = {
            "lat": crd[0],
            "lon": crd[1],
            "appid": 'a98acb72049c5a83be4989a69821f380',
        }
        response = requests.get(url=API_OWM_PROG, params=params)
        data_w = response.json()
        return data_w

