import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
import os 
from main import set_wallpaper
import threading
import json
import sys
import subprocess

def save_scheduler_config(config):
    with open("scheduler_config.json", "w") as f:
        json.dump(config, f, indent=4)

def load_scheduler_config(): 
    try:
        with open("scheduler_config.json") as f:
            return json.load(f)  
    except:
        return {}         
#here i took help from ai cause i don't knew much how does scheduling works using script
def create_or_update_scheduled_task(interval_hours):
    task_name = "OtakuWalL_Wallpaper_Scheduler"
    python_exe = sys.executable.replace("python.exe", "pythonw.exe")  
    script_path = os.path.abspath("scheduler.py")

    subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], capture_output=True)

    base_cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'"{python_exe}" "{script_path}"',
        "/f",
        "/ru", os.environ.get("USERNAME"),
        "/rl", "LIMITED",
    ]

    if interval_hours < 1:
        interval_minutes = max(int(interval_hours * 60), 1)
        cmd = base_cmd + ["/sc", "minute", "/mo", str(interval_minutes)]
    else:
        cmd = base_cmd + ["/sc", "hourly", "/mo", str(int(interval_hours))]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def delete_scheduled_task():
    task_name = "OtakuWalL_Wallpaper_Scheduler"
    subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], capture_output=True)

def main():
    ctk.set_appearance_mode('system')
    ctk.set_default_color_theme('green')
    root = ctk.CTk()
    root.geometry("700x550")

    selected_custom_image_path = None 

    ctk.FontManager.load_font(r"assets/fonts/font1.ttf") 

    frame = ctk.CTkFrame(master=root)
    frame.pack(padx=20, pady=10, expand=True, fill="both")

    container_Type_wallpaper_label = ctk.CTkFrame(frame, fg_color='transparent')
    container_Type_wallpaper_label.pack(padx=20, pady=10)

    container_cusom_input_text = ctk.CTkFrame(frame,fg_color='transparent')
    container_cusom_input_text.pack(padx=20, pady=10)

    container_Type_quote_label = ctk.CTkFrame(frame, fg_color='transparent')
    container_Type_quote_label.pack(padx=20, pady=10)


    
    container_time_based_schedule = ctk.CTkFrame(frame, fg_color='transparent')
    container_time_based_schedule.pack(padx=20, pady=10)

    container_custom_quote_input_label = ctk.CTkFrame(frame, fg_color='transparent')
    container_custom_quote_input_label.pack(padx=20, pady=10)

    container_city_input_label = ctk.CTkFrame(frame, fg_color='transparent')
    container_city_input_label.pack(padx=20, pady=10)

    container_time_based_greetings_label = ctk.CTkFrame(frame, fg_color='transparent')
    container_time_based_greetings_label.pack(padx=20, pady=10)

    def handle_schedule_and_save():
        nonlocal selected_custom_image_path
        
        schedule_val = optionmenu_schedule.get() 
        if schedule_val == "Don't change":
            interval_hours = 0
        else:
            parts = schedule_val.split()
            if len(parts) >= 2:
                val_str = parts
                interval_hours = float(parts[1])
            else:
                interval_hours = 0
                
        config = {
            "schedule_enabled": interval_hours > 0,
            "genre": custom_wallpaper_input.get(),
            "interval_hours": interval_hours,
            "wallpaper_type": optionmenu_wallpaper.get(),
            "quote_type": optionmenu_quote.get(),
            "city": city_input.get(),
            "use_time_greetings": time_based_greetings_label.get(),
            "custom_quote": custom_quote_input.get(),
            "custom_path": selected_custom_image_path if selected_custom_image_path else None
        }   

        if config["wallpaper_type"] == "custom":
            config["schedule_enabled"] = False
            interval_hours = 0 

        save_scheduler_config(config)

        if interval_hours > 0:
            success = create_or_update_scheduled_task(interval_hours)
            if success:
                messagebox.showinfo("Scheduled", f"Wallpaper will update every {interval_hours} hour(s).")
            else:
                messagebox.showerror("Error", "Failed to create scheduled task.")
        else:
            subprocess.run(["schtasks", "/delete", "/tn", "OtakuWalL_Wallpaper_Scheduler", "/f"], capture_output=True)
            messagebox.showinfo("Scheduler Disabled", "Wallpaper scheduling is disabled.")
            
        thread = threading.Thread(target=wallpaper_set)
        thread.daemon = True
        thread.start()

    def wallpaper_set_resp():
        nonlocal selected_custom_image_path
        
        if optionmenu_wallpaper.get() == "custom" and not selected_custom_image_path:
            messagebox.showerror("hmm", "Upload an image first! lol")
            return
        if optionmenu_wallpaper.get() == "Select":
            messagebox.showerror("hmm", "Select the type of wallpaper!!, first")
            return

        thread = threading.Thread(target=wallpaper_set) 
        thread.daemon = True 
        thread.start()  

    def wallpaper_set():
        nonlocal selected_custom_image_path
        
        try:
            wallpaper_type = optionmenu_wallpaper.get()
            genre = custom_wallpaper_input.get()
            quote_type = optionmenu_quote.get()
            city_name = city_input.get()
            is_greetings = time_based_greetings_label.get()
            custom_quote = custom_quote_input.get()

            if wallpaper_type == "custom":
               set_wallpaper(type=wallpaper_type, custom_path=selected_custom_image_path, 
                           custom_quote=custom_quote, category=wallpaper_type, 
                           quote_type=quote_type, city=city_name, use_time_greetings=is_greetings,genre=genre)
            else:
               set_wallpaper(type=wallpaper_type, custom_path=None, custom_quote=None, 
                           category=wallpaper_type, quote_type=quote_type, 
                           city=city_name, use_time_greetings=is_greetings,genre=genre)
            
            root.after(0, lambda: on_finish_success())
        except Exception as e:
            root.after(0, lambda: on_finish_error(str(e)))

    def on_finish_success():
        btn.configure(text='Set!!', state="normal")
        messagebox.showinfo("Success", "Wallpaper Set Successfully!!")
        reset_ui()

    def on_finish_error(e):
        btn.configure(text='Set!!', state="normal")
        messagebox.showerror("Error", f'Failed to set wallpaper:\n{e}')

    def reset_ui():
            optionmenu_quote.configure(state='normal')
            custom_wallpaper_input.delete(0, 'end')
            custom_wallpaper_input.configure(state = 'disabled')
            btn_upload_wallpaper_img.pack_forget()
            btn_upload_wallpaper_img.configure(state='disabled')
            custom_quote_input.delete(0, 'end')
            custom_quote_input.configure(state='disabled')
            time_based_greetings_label.configure(state='normal') 
            city_input.configure(state='normal')
            optionmenu_schedule.configure(state='normal')
            optionmenu_quote.set("None")
            optionmenu_wallpaper.set("Select")
            optionmenu_schedule.set("Don't change")


            file_name_label.configure(text="")
            file_name_label.pack_forget()
            selected_custom_image_path = None


        
    def options_menu(choice):
        nonlocal selected_custom_image_path
        
        if choice == "custom":
            btn_upload_wallpaper_img.pack(side='left', padx=10)
            btn_upload_wallpaper_img.configure(state='normal') 
            custom_quote_input.configure(state='normal')
            time_based_greetings_label.configure(state='disabled')
            optionmenu_schedule.configure(state='disabled')
            optionmenu_quote.configure(state='disabled')
            city_input.configure(state='disabled')
            custom_wallpaper_input.configure(state = 'disabled')


        elif choice == "type a genre":
            optionmenu_quote.configure(state='disabled')
            custom_wallpaper_input.configure(state = 'normal')
            custom_input_label.configure(state = 'normal')
            btn_upload_wallpaper_img.configure(state='disabled') 
            custom_quote_input.configure(state='disabled')
            time_based_greetings_label.configure(state='normal') 
            custom_quote_input.delete(0, 'end')
            btn_upload_wallpaper_img.pack_forget()
            file_name_label.configure(text="")
            file_name_label.pack_forget()
            selected_custom_image_path = None

        else:
            custom_wallpaper_input.configure(state = 'disabled')
            time_based_greetings_label.configure(state='normal') 
            custom_input_label.configure(state = 'disabled')
            optionmenu_quote.configure(state='normal')
            city_input.configure(state='normal')
            optionmenu_schedule.configure(state='normal')
            custom_quote_input.delete(0, 'end')
            btn_upload_wallpaper_img.configure(state='disabled') 
            custom_quote_input.configure(state='disabled')
            btn_upload_wallpaper_img.pack_forget()
            file_name_label.configure(text="")
            file_name_label.pack_forget()
            selected_custom_image_path = None

        print("optionmenu dropdown clicked:", choice)

    def ImageOpen():
        nonlocal selected_custom_image_path
        
        selected_custom_image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if selected_custom_image_path:
            filename = os.path.basename(selected_custom_image_path)
            file_name_label.configure(text=filename)
            file_name_label.pack(side='left', padx=10)   
            messagebox.showinfo('Uploaded', f'Image {filename} uploaded')
            btn.configure(state='normal') 

    Header = ctk.CTkLabel(container_Type_wallpaper_label, text='OtakuWalL', font=("Oswald Light", 24))
    Header.pack()

    Type_wallpaper_label = ctk.CTkLabel(container_Type_wallpaper_label, text='Select the type of wallpaper:', 
                                      fg_color="transparent", font=("Oswald ExtraLight", 15))
    Type_wallpaper_label.pack(side='left', padx=10, pady=5)

    optionmenu_wallpaper = ctk.CTkOptionMenu(container_Type_wallpaper_label, 
                                           values=["Select","Anime","Movie","Nature","custom","type a genre"], 
                                           command=options_menu, font=("Oswald ExtraLight", 15))
    
    optionmenu_wallpaper.set("Select")
    optionmenu_wallpaper.pack(side='left', pady=10)

    btn_upload_wallpaper_img = ctk.CTkButton(container_Type_wallpaper_label, text='Upload Image', 
                                           command=lambda: ImageOpen())
    btn_upload_wallpaper_img.configure(state='disabled')

    file_name_label = ctk.CTkLabel(container_Type_wallpaper_label, text='', font=("Oswald ExtraLight", 15))
    

    custom_input_label = ctk.CTkLabel(container_cusom_input_text, text='Enter your custom genre:', font=("Oswald ExtraLight", 15))
    custom_input_label.pack(side='left')


    custom_wallpaper_input = ctk.CTkEntry(container_cusom_input_text, font=("Oswald ExtraLight",15))
    custom_wallpaper_input.pack(side='left', padx=5)
    custom_wallpaper_input.configure(state='disabled')

    quote_label = ctk.CTkLabel(container_Type_quote_label, text='Quote (optional):', font=("Oswald ExtraLight", 15))
    quote_label.pack(side='left')

    optionmenu_quote = ctk.CTkOptionMenu(container_Type_quote_label, values=["None","Default"], 
                                       font=("Oswald ExtraLight", 15))
    optionmenu_quote.set("None")
    optionmenu_quote.pack(side='left', padx=10)

    custom_quote_label = ctk.CTkLabel(container_custom_quote_input_label, text='Enter your custom quote:', 
                                    font=("Oswald ExtraLight",15))
    custom_quote_label.pack(side='left')

    custom_quote_input = ctk.CTkEntry(container_custom_quote_input_label, font=("Oswald ExtraLight",15))
    custom_quote_input.pack(side='left', padx=5)
    custom_quote_input.configure(state='disabled')

    city_label = ctk.CTkLabel(container_city_input_label, text='Enter city for weather (optional):', 
                            font=("Oswald ExtraLight",15))
    city_label.pack(side='left')

    city_input = ctk.CTkEntry(container_city_input_label, font=("Oswald ExtraLight",15))
    city_input.pack(side='left', padx=5)

    schedule_label = ctk.CTkLabel(container_time_based_schedule, text='Select how often wallpaper should change:', 
                                font=("Oswald ExtraLight",15))
    schedule_label.pack(side='left')

    optionmenu_schedule = ctk.CTkOptionMenu(container_time_based_schedule, 
                                          values=["Don't change", "every 0.02 hours(for testing)",
                                                  "every 2 hours", "every 5 hours", 
                                                "every 10 hours", "every 24 hours"], 
                                          font=("Oswald ExtraLight", 15))
    optionmenu_schedule.set("Don't change")
    optionmenu_schedule.pack(side='left', padx=10)

    time_based_greetings_label = ctk.CTkCheckBox(container_time_based_greetings_label, text='Time based greetings', 
                                               font=("Oswald ExtraLight", 15))
    time_based_greetings_label.pack(pady=5)

    btn = ctk.CTkButton(master=frame, text='Set!!', command=handle_schedule_and_save)
    btn.pack(padx=20, pady=30)

    root.mainloop()

if __name__ == "__main__":
    main()
