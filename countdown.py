"""
Daniel Vogler
countdown app
"""

import tkinter as tk
from tkinter import *

import os
from threading import Thread


class CountdownApp(tk.Frame):  

    
    ### initialize
    def __init__(self,master):

        self.definitions()
        app.geometry(self.window_resolution)
        app.configure(bg=self.color_background) 

        tk.Frame.__init__(self, master)
        self.master = master
        self.app_running = False
        self.sound_on = False
        self.gui()


    ### construct window
    def gui(self):

        ### enter and set time
        self.entry = Entry(self.master, width=10, font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, relief="flat", justify='center')
        self.submit_button = Button(self.master, text="Set time", font=(self.font_type, self.font_size_button), fg=self.font_color_text, bg=self.color_background, borderwidth=0, highlightthickness=0, command = self.parse_input )

        ### set sound frequency
        self.entry_sound = Entry(self.master, width=10, font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, relief="flat", justify='center')
        self.set_sound_button = Button(self.master, text="Set sound", font=(self.font_type, self.font_size_button), fg=self.font_color_text, bg=self.color_background, borderwidth=0, highlightthickness=0, command = self.set_sound )

        ### time display
        self.time_display = Label(self.master, text="00:00:00", font=(self.font_type, self.font_size_time_display), borderwidth=2, fg=self.font_color_time_display, bg=self.color_background)

        ### start countdown button
        self.start_button = Button(self.master, text="Start", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.start)

        ### close window button
        self.close_button = Button(self.master, text="Close", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.master.quit)

        ### turn sound ON/OFF
        self.sound_button = Button(self.master, text="Sound OFF", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.sound)

        ### layout
        self.time_display.place(relx=0.5, rely=0.5, anchor=CENTER)
        ### layout - set time
        self.entry.place(relx=0.2, rely=0.1, anchor=CENTER)
        self.submit_button.place(relx=0.2, rely=0.2, anchor=CENTER)
        ### layout - set sound frequency
        self.entry_sound.place(relx=0.8, rely=0.1, anchor=CENTER)
        self.set_sound_button.place(relx=0.8, rely=0.2, anchor=CENTER)
        ### layout - sound on/off
        self.sound_button.place(relx=0.3, rely=0.9, anchor=CENTER)
        self.start_button.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.close_button.place(relx=0.7, rely=0.9, anchor=CENTER)


    ### get time from entry field
    def parse_input(self):

        self.total_time = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        
        parsed_time = self.entry.get().split(":")

        if len(parsed_time) == 1:
            self.seconds = int(parsed_time[-1])
        elif len(parsed_time) == 2:
            self.seconds = int(parsed_time[-1])
            self.minutes = int(parsed_time[-2])
        elif len(parsed_time) == 3:
            self.seconds = int(parsed_time[-1])
            self.minutes = int(parsed_time[-2])
            self.hours = int(parsed_time[-3])

        self.set_time = self.seconds + self.minutes*60 + self.hours*3600
        self.time = self.set_time
        print("Set time:", self.set_time)

        self.update_time_display()

        return self.set_time


    ### update time display
    def update_time_display(self):

        self.seconds = self.time % 60
        self.minutes = ( self.time // 60 ) % 60
        self.hours = self.time // 3600
        if (self.set_time - self.time) % self.sound_frequency == 0 and (self.set_time - self.time) != 0 and self.sound_on:
            self.play_sound(0.2, 600) 
        
        self.time_string = "{:02d}:{:02d}:{:02d}".format(self.hours, self.minutes, self.seconds)
        self.time_display.configure(text=self.time_string, fg = self.font_color_time_display)


    ### start countdown
    def start(self):

        self.start_button.configure(text="Stop", command=lambda: self.stop())
        if self.sound_on:
            self.play_sound(0.2, 600)

        self.app_running = True
        self.update_time()


    ### turn sound on and off
    def sound(self):

        if self.sound_on:
            self.sound_button.configure(text="Sound OFF")
            self.sound_on = False

        elif self.sound_on == False:
            self.sound_button.configure(text="Sound ON")
            self.sound_on = True
            self.play_sound(0.2, 600)


    ### set sound signal frequency
    def set_sound(self):

        self.sound_frequency = int(self.entry_sound.get())


    ### play sound
    def play_sound(self, duration, frequency):
        os.system('play -n synth %s sin %s' % (duration, frequency))


    ### update time 
    def update_time(self):

        if self.app_running:
            if self.time <= 0:
                self.time_display.configure(text="Finished", fg=self.color_end)
                self.start_button.configure(text="Start")
                if self.sound_on:
                    self.play_sound(1.0, 600)
    
            else:
                self.time -= 1
                self.time_display.configure(text=self.update_time_display())
                self.after(1000, self.update_time)


    ### pause countdown
    def stop(self):

        self.start_button.configure(text="Start", command=lambda: self.start())
        self.app_running = False
        self.update_time


    ### definitions
    def definitions(self):
        self.color_background = "black"
        self.color_end = "green"
        self.font_color_time_display = "red"
        self.font_color_text = "white"
        self.font_size_time_display = 200
        self.font_size_button = 40
        self.button_borderwidth = 5
        self.window_resolution = "2000x1400"
        self.font_type = "Helvetica"
        self.sound_frequency = 3600


if __name__ == "__main__":
    app = Tk()
    my_gui = CountdownApp(app)
    app.title("Countdown timer")
    app.mainloop()