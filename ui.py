import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
import os 
from main import set_wallpaper
ctk.set_appearance_mode('system')
ctk.set_default_color_theme('green')
root = ctk.CTk()
root.geometry("700x500")



frame = ctk.CTkFrame(master=root)
frame.pack(padx= 20, pady = 10, expand=True, fill="both")

container_Type_wallpaper_label= ctk.CTkFrame(frame,fg_color='transparent')
container_Type_wallpaper_label.pack(padx=20,pady=10)

container_Type_wallpaper_label_img = ctk.CTkFrame(container_Type_wallpaper_label,fg_color='transparent')
container_Type_wallpaper_label_img.forget()


container_Type_quote_label = ctk.CTkFrame(frame,fg_color='transparent')
container_Type_quote_label.pack(padx=20,pady=10)

container_custom_quote_input_label = ctk.CTkFrame(frame,fg_color='transparent')
container_custom_quote_input_label.pack(padx = 20, pady = 10)

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
    custom_quote = custom_quote_input.get()
    if wallpaper_type == "custom":
       set_wallpaper(type=wallpaper_type,custom_path = selected_custom_image_path, custom_quote =custom_quote, category=wallpaper_type,quote_type=quote_type,city=city_name,use_time_greetings=is_greetings)
    else:
       set_wallpaper(type=wallpaper_type,custom_path =None,custom_quote=None,category=wallpaper_type,quote_type=quote_type,city=city_name,use_time_greetings=is_greetings)
    

    
Header = ctk.CTkLabel(container_Type_wallpaper_label,text='OtakuWalL',font=("Oswald Light", 24))
Header.pack()

def options_menu(choice):
    if choice == "custom" :
        # container_Type_wallpaper_label_img.pack(padx = 20, pady = 10)

        btn_upload_wallpaper_img.pack(side='left',padx=10)

        btn_upload_wallpaper_img.configure(state='normal') 
        custom_quote_input.configure(state = 'normal')
        time_based_greetings_label.configure(state ='disabled' )
        optionmenu_quote.configure(state = 'disabled')
        city_input.configure(state = 'disabled')
        # if   file_name_label:
        #      messagebox.showinfo('Uploaded', 'Image uploaded') 
             


    else :
        time_based_greetings_label.configure(state ='normal' ) 
        optionmenu_quote.configure(state = 'normal')
        city_input.configure(state = 'normal')
        btn_upload_wallpaper_img.configure(state='disabled') 
        custom_quote_input.configure(state = 'disabled')
        optionmenu_quote.configure(state = 'normal')
        container_Type_wallpaper_label_img.pack_forget()
        file_name_label.configure(text="")

    print("optionmenu dropdown clicked:", choice)

def ImageOpen():
        global selected_custom_image_path
        selected_custom_image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if selected_custom_image_path:
            filename = os.path.basename(selected_custom_image_path)
            file_name_label.configure(text=filename)
            messagebox.showinfo('Uploaded', f'Image {filename} uploaded')
                

           
Type_wallpaper_label = ctk.CTkLabel(container_Type_wallpaper_label,text='Select the type of wallpaper:',fg_color="transparent",font=("Oswald ExtraLight", 15))
Type_wallpaper_label.pack(side='left',padx=10,pady=5)

optionmenu_wallpaper = ctk.CTkOptionMenu(container_Type_wallpaper_label,values=["Select","Anime","Movie","Nature","custom"],command=options_menu,font=("Oswald ExtraLight", 15))
optionmenu_wallpaper.set("Select")
optionmenu_wallpaper.pack(side='left',pady=10)

btn_upload_wallpaper_img = ctk.CTkButton(container_Type_wallpaper_label,text='Upload Image',command=lambda: ImageOpen())
btn_upload_wallpaper_img.pack(side='left',padx=10)
btn_upload_wallpaper_img.configure(state = 'disabled')

file_name_label = ctk.CTkLabel(container_Type_wallpaper_label,text='',font=("Oswald ExtraLight", 15))


quote_label = ctk.CTkLabel(container_Type_quote_label,text='Quote (optional):',font=("Oswald ExtraLight", 15))
quote_label.pack(side='left')


optionmenu_quote = ctk.CTkOptionMenu(container_Type_quote_label,values=["None","Default"],font=("Oswald ExtraLight", 15))
optionmenu_quote.set("None")
optionmenu_quote.pack(side='left',padx=10)


custom_quote_label = ctk.CTkLabel(container_custom_quote_input_label,text='Enter your custom quote:',font=("Oswald ExtraLight",15))
custom_quote_label.pack(side = 'left')

custom_quote_input = ctk.CTkEntry(container_custom_quote_input_label,font=("Oswald ExtraLight",15))
custom_quote_input.pack(side='left', padx=5)
custom_quote_input.configure(state = 'disabled')


city_label = ctk.CTkLabel(container_city_input_label,text='Enter city for weather (optional):',font=("Oswald ExtraLight",15))
city_label.pack(side = 'left')

city_input = ctk.CTkEntry(container_city_input_label,font=("Oswald ExtraLight",15))
city_input.pack(side='left', padx=5)





time_based_greetings_label = ctk.CTkCheckBox(container_time_based_greetings_label,text='Time based greetings',font=("Oswald ExtraLight", 15))
time_based_greetings_label.pack(pady=5)

btn = ctk.CTkButton(master=frame,text='Set!!',command=wallpaper_set)
btn.pack(padx=20,pady=30)

root.mainloop()