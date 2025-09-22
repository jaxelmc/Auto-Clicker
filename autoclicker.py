import customtkinter
import os
import tkinter as tk
import pyautogui
import keyboard
import threading
from tkinter import messagebox
os.system('cls')

class MainProgram():
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title("Auto Clicker")
        self.root.minsize(560, 230)
        self.root.maxsize(560, 230)
        self.root.iconbitmap("cursor.ico")
        self.root.grid_columnconfigure(0, weight=1)
        self.mousex = None
        self.mousey = None
        self.keybind = None
        #Program running or not
        self.program = False

        #Delay Frame
        self.delay_f = customtkinter.CTkFrame(self.root, fg_color="transparent")
        for i in range(0, 6):
            self.delay_f.grid_columnconfigure(i, weight=1)
        self.delay_f.grid(row=0, column=0, pady=20, sticky='ew')

        #Minute
        self.min_tb = customtkinter.CTkTextbox(self.delay_f, width=100, height= 15, font=("Helvetica", 20), border_spacing=0, corner_radius=1, border_width=1, activate_scrollbars=False)
        self.min_tb.grid(row=0, column=0, sticky='e')
        self.min_tb.bind('<KeyPress>', lambda event: self.number_limit_fun(event, self.min_tb))
        self.min_lb = customtkinter.CTkLabel(self.delay_f, text="Minute", fg_color="transparent",padx=10 )
        self.min_lb.grid(row=0, column=1, sticky='w')
        #Seconds
        self.sec_tb = customtkinter.CTkTextbox(self.delay_f, width=100, height= 15, font=("Helvetica", 20), border_spacing=0, corner_radius=1, border_width=1, activate_scrollbars=False)
        self.sec_tb.grid(row=0, column=2, sticky='e')
        self.sec_tb.bind('<KeyPress>', lambda event: self.number_limit_fun(event, self.sec_tb))
        self.sec_lb = customtkinter.CTkLabel(self.delay_f, text="Second", fg_color="transparent",padx=10 )
        self.sec_lb.grid(row=0, column=3, sticky='w')
        #Mili Seconds
        self.milis_tb = customtkinter.CTkTextbox(self.delay_f, width=100, height= 15, font=("Helvetica", 20), border_spacing=0, corner_radius=1, border_width=1, activate_scrollbars=False)
        self.milis_tb.grid(row=0, column=4, sticky='e')
        self.milis_tb.bind('<KeyPress>', lambda event: self.number_limit_fun(event, self.milis_tb))
        self.milis_lb = customtkinter.CTkLabel(self.delay_f, text="Millisecond", fg_color="transparent",padx=10 )
        self.milis_lb.grid(row=0, column=5, sticky='w')


        #--------------------|MIDDLE FRAME|--------------------#
        self.middle_f = customtkinter.CTkFrame(self.root, fg_color="transparent")
        for i in range(3, 6):
            self.middle_f.grid_columnconfigure(i, weight=1)
        self.middle_f.grid(row=1, column=0, pady=40, padx=14, sticky='ew')

        #Click CheckBoxes
        self.click_inf_cb = customtkinter.CTkCheckBox(self.middle_f, text="Infinite Clicks", command=self.inf_cb_fun)
        self.click_inf_cb.grid(row=0, column=0)
        self.click_amount_cb = customtkinter.CTkCheckBox(self.middle_f, text="Limited Clicks:", command=self.amount_cb_fun)
        self.click_amount_cb.grid(row=0, column=1, padx=20)
        #Click Amount
        self.click_amount_tb = customtkinter.CTkTextbox(self.middle_f, width=80, height= 15, font=("Helvetica", 15), border_spacing=0, corner_radius=1, border_width=1, activate_scrollbars=False, wrap='none')
        self.click_amount_tb.grid(row=0, column=2, sticky='w')
        self.click_amount_tb.bind('<KeyPress>', self.amount_tb_text_replace_fun)
        #Start Stop Keybind
        self.keybind_btn = customtkinter.CTkButton(self.middle_f,command=self.set_keybind_fun, text="Start/Stop Keybind", font=("Helvetica", 15), corner_radius=3)
        self.keybind_btn.grid(row=0, column=4, sticky='nsew')

        #SET DEFAULT 
        self.click_inf_cb.select()


        #--------------------|BOTTOM FRAME|--------------------#
        self.bottom_f = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.bottom_f.grid(row=2, column=0, padx=14, sticky='ew')
        self.bottom_f.grid_columnconfigure(3, weight=1)
        self.bottom_f.grid_columnconfigure(4, weight=1)

        #Click Location
        self.click_location_cb = customtkinter.CTkCheckBox(self.bottom_f, text="Click at Cords", command=self.click_location_fun)
        self.click_location_cb.grid(row=0, column=0)
        #Click Coordinates Button
        self.click_cords_btn = customtkinter.CTkButton(self.bottom_f, text="Set Coordinate", corner_radius=2, height=15, width=110, command=self.get_mouse_cords_fun)
        self.click_cords_btn.grid(row=0, column=1, padx=20)
        #Write Coordinates
        self.click_cords_tb = customtkinter.CTkTextbox(self.bottom_f, width=80, height= 15, font=("Helvetica", 13), border_spacing=0, corner_radius=1, border_width=1, activate_scrollbars=False, wrap='none')
        self.click_cords_tb.grid(row=0, column=2, padx=5)
        self.click_cords_tb.insert("0.0", "'X' Set Cords")
        #Start Stop Button
        self.start_stop_btn = customtkinter.CTkButton(self.bottom_f, text="Start/Stop", font=("Helvetica", 15), corner_radius=4, command=self.click, height=35)
        self.start_stop_btn.grid(row=0, column=3, sticky='nsew', padx=(10, 0))
        self.start_stop_btn.bind('<Enter>', self.start_stop_hover_fun)
        self.start_stop_btn.bind('<Leave>', self.start_stop_unhover_fun)
        self.program_stat_tb = customtkinter.CTkTextbox(self.bottom_f, state="disabled", width=5, height= 1,border_spacing=0, corner_radius=11, bg_color=self.start_stop_btn.cget("fg_color"), font=("Helvetica", 1), fg_color="#a10202", border_color="black", border_width=2)
        self.program_stat_tb.grid(row=0, column=3, sticky='e', padx=(0, 2))
        

        self.root.mainloop()
    
    #----------------------------------------------------------------------------------------------------


    #Get Mouse Coordinates
    def get_mouse_cords_fun(self):
            keyboard.wait('x')
            self.mousex, self.mousey = pyautogui.position()
            self.current_mouse_position = self.mousex,"x",self.mousey
            self.click_cords_tb.delete("0.0", "end")
            self.click_cords_tb.insert("0.0",self.current_mouse_position)


    #Don't let clicks at cords if cords not choosen
    def click_location_fun(self):
        if self.mousex==None and self.mousey==None:
            self.click_location_cb.deselect()
            messagebox.showinfo("Invalid Coordinates", "Set Coordinates first",detail="Click Set Coordinate button \nPress 'X' once in Position", icon='warning')


    #Program Status box color change 
    def start_stop_hover_fun(self, event):
        self.program_stat_tb.configure(bg_color="#144870")
    def start_stop_unhover_fun(self, event):
        self.program_stat_tb.configure(bg_color=self.start_stop_btn.cget("fg_color"))

    #Inf/Amount Checkbox Toggle
    def inf_cb_fun(self):
        print(self)
        if(self.click_inf_cb.get()==1):
            self.click_amount_cb.deselect()
        if(self.click_inf_cb.get()==0):
            self.click_inf_cb.select()
    def amount_cb_fun(self):
        if(self.click_amount_cb.get()==1):
            self.click_inf_cb.deselect()
        if(self.click_amount_cb.get()==0):
            self.click_inf_cb.select()

    #Limit the delay boxes to only numbers and 7 digits
    def number_limit_fun(self, event, box):
        count=(len(box.get("0.0", "end").strip("\n")))
        if count >= 7 and event.keysym not in {'BackSpace', 'Delete'} or (not event.char.isdigit() and event.keysym not in {'BackSpace', 'Delete'}):
            return 'break'  
    #Limit the click amout text box to only numbers
    def amount_tb_text_replace_fun(self,event):
         if event.keysym not in {'BackSpace', 'Delete'} and not event.char.isdigit():
          return 'break'
    
    #Set Keybind
    def set_keybind_fun(self):
        self.keybind_btn.configure(fg_color="#144870")
        self.keybind=keyboard.read_hotkey()
        self.keybind_btn.configure(fg_color=self.start_stop_btn.cget("fg_color"))
        print("Hello World")
        

    #Run Auto Clicking
    def click(self):
         #Check for Start or Stop and Change the Stats color
         self.program = not self.program
         if self.program == True:
             self.program_stat_tb.configure(fg_color="green")
         else:
             self.program_stat_tb.configure(fg_color="#a10202")

         self.click_amount = (self.click_amount_tb.get("0.0", "end").strip(" \n")).replace(" ","")
         print("position = ",self.mousex, self.mousey)
         print(f"times = {self.click_amount}")
         print(f"Start Stop Keybind: {self.keybind}")

           
         

MainProgram()

