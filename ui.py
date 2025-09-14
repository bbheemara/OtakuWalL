import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkfont
import os 


ctk.set_appearance_mode('system')
ctk.set_default_color_theme('green')
root = ctk.CTk()
root.geometry("600x600")



frame = ctk.CTkFrame(master=root)
frame.pack(padx= 20, pady = 10, expand=True, fill="both")

container_Type_wallpaper_label= ctk.CTkFrame(frame,fg_color='transparent')
container_Type_wallpaper_label.pack(padx=20,pady=5)


container_time_based_greetings_label = ctk.CTkFrame(frame,fg_color='transparent')
container_time_based_greetings_label.pack(padx=20,pady=5)

container_city_input_label = ctk.CTkFrame(frame,fg_color='transparent')
container_city_input_label.pack(padx=20,pady=5)

container_Type_quote_label = ctk.CTkFrame(frame,fg_color='transparent')
container_Type_quote_label.pack(padx=20,pady=5)




ctk.FontManager.load_font(r"assets/fonts/font1.ttf")




Header = ctk.CTkLabel(container_Type_wallpaper_label,text='OtakuWal',font=("Oswald Light", 24))
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


optionmenu_quote = ctk.CTkOptionMenu(container_Type_quote_label,values=["Anime","Movie","Nature","Select"],font=("Oswald ExtraLight", 15))
optionmenu_quote.set("Select")
optionmenu_quote.pack(side='left',padx=5)

city_label = ctk.CTkLabel(container_city_input_label,text='Enter city for weather (optional):',font=("Oswald ExtraLight",15))
city_label.pack(side = 'left')

city_input = ctk.CTkEntry(container_city_input_label,font=("Oswald ExtraLight",15))
city_input.pack(side='left', padx=5)





time_based_greetings_label = ctk.CTkCheckBox(container_time_based_greetings_label,text='Time based greetings',font=("Oswald ExtraLight", 15))
time_based_greetings_label.pack(pady=5)
# btn = ctk.CTkButton(master=frame,text='Set!!')
# btn.pack(padx=20,pady=60)

root.mainloop()