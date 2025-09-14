import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkfont
import os 
from main import set_wallpaper

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('green')
root = ctk.CTk()
root.geometry("500x500")



frame = ctk.CTkFrame(master=root)
frame.pack(padx= 20, pady = 10, expand=True, fill="both")

container_Type_wallpaper_label= ctk.CTkFrame(frame,fg_color='transparent')
container_Type_wallpaper_label.pack(padx=20,pady=10)

container_Type_quote_label = ctk.CTkFrame(frame,fg_color='transparent')
container_Type_quote_label.pack(padx=20,pady=10)

container_city_input_label = ctk.CTkFrame(frame,fg_color='transparent')
container_city_input_label.pack(padx=20,pady=10)

container_time_based_greetings_label = ctk.CTkFrame(frame,fg_color='transparent')
container_time_based_greetings_label.pack(padx=20,pady=10)



ctk.FontManager.load_font(r"assets/fonts/font1.ttf")


def wallpaper_set():
    wallpaper_type = optionmenu_wallpaper.get()
    quote_type = optionmenu_quote.get()
    city_name = city_input.get()
    is_greetings = time_based_greetings_label.get()

    set_wallpaper(type=wallpaper_type,city=city_name,use_time_greetings=is_greetings)
    

Header = ctk.CTkLabel(container_Type_wallpaper_label,text='OtakuWalL',font=("Oswald Light", 24))
Header.pack()
def options_menu(choice):
    print("optionmenu dropdown clicked:", choice)

Type_wallpaper_label = ctk.CTkLabel(container_Type_wallpaper_label,text='Select the type of wallpaper:',fg_color="transparent",font=("Oswald ExtraLight", 15))
Type_wallpaper_label.pack(side='left',padx=10,pady=5)


optionmenu_wallpaper = ctk.CTkOptionMenu(container_Type_wallpaper_label,values=["Anime","Movie","Nature"],command=options_menu,font=("Oswald ExtraLight", 15))
optionmenu_wallpaper.set("Nature")
optionmenu_wallpaper.pack(side='left',pady=10)

quote_label = ctk.CTkLabel(container_Type_quote_label,text='Quote (optional):',font=("Oswald ExtraLight", 15))
quote_label.pack(side='left')


optionmenu_quote = ctk.CTkOptionMenu(container_Type_quote_label,values=["Anime Quotes","Movie Quotes","Famouse Quotes","Select"],font=("Oswald ExtraLight", 15))
optionmenu_quote.set("Select")
optionmenu_quote.pack(side='left',padx=10)

city_label = ctk.CTkLabel(container_city_input_label,text='Enter city for weather (optional):',font=("Oswald ExtraLight",15))
city_label.pack(side = 'left')

city_input = ctk.CTkEntry(container_city_input_label,font=("Oswald ExtraLight",15))
city_input.pack(side='left', padx=5)





time_based_greetings_label = ctk.CTkCheckBox(container_time_based_greetings_label,text='Time based greetings',font=("Oswald ExtraLight", 15))
time_based_greetings_label.pack(pady=5)

btn = ctk.CTkButton(master=frame,text='Set!!',command=wallpaper_set)
btn.pack(padx=20,pady=30)

root.mainloop()