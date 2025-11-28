import threading
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from tkinter import Toplevel
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# Path to your ChromeDriver
CHROMEDRIVER_PATH = "./chromedriver/chromedriver.exe"

# Driver function
def create_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # uncomment for headless
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

# Scraper itself
def scroll_until_all_hotels_loaded(driver, max_wait_time=10): # change max_wait_time to your liking
    SCROLL_PAUSE_TIME = 2.5
    last_count = 0
    start_time = time.time()
    while True:
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(SCROLL_PAUSE_TIME)
        hotels = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
        current_count = len(hotels)
        print(f"Visible hotels: {current_count}")
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, 'button.bbf83acb81')
            if load_more_button.is_displayed():
                print("Clicking 'Load more' button...")
                load_more_button.click()
                time.sleep(SCROLL_PAUSE_TIME)
        except NoSuchElementException:
            pass
        except ElementClickInterceptedException:
            # Sometimes a popup overlaps the button
            print("Button click blocked. Retrying...")
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            time.sleep(1)
            load_more_button.click()
            time.sleep(SCROLL_PAUSE_TIME)

        if current_count > last_count:
            last_count = current_count
            start_time = time.time()
        else:
            if time.time() - start_time > max_wait_time:
                print("Stop scrolling: no new hotels after 10 seconds.")
                break
    return hotels

# Extracting data 
def extract_hotels(driver):
    hotels = scroll_until_all_hotels_loaded(driver)
    hotel_list = []
    for hotel in hotels:
        data = {}
        try: data['Hotel Name'] = hotel.find_element(By.XPATH, './/div[@data-testid="title"]').text
        except: data['Hotel Name'] = 'N/A'
        '''
        try:
            stars = len(hotel.find_elements(By.XPATH, './/div[@data-testid="rating-stars"]/span'))
            data['Stars'] = stars
        except:
            data['Stars'] = 'N/A'
        '''
        try:
            price = hotel.find_element(By.XPATH, './/span[@data-testid="price-and-discounted-price"]').text
            price_clean = re.sub(r'[^\d,]', '', price).replace(',', '.')
            data['Price'] = float(price_clean) if price_clean else 'N/A'
        except: data['Price'] = 'N/A'
        try:
            note_elem = hotel.find_element(By.XPATH, './/div[contains(@class, "f63b14ab7a")]')
            note = note_elem.text.strip()
            data['Review Score (/10)'] = float(note.replace(',', '.'))
        except: data['Review Score (/10)'] = 'N/A'
        try:
            link = hotel.find_element(By.XPATH, './/a[@data-testid="title-link"]').get_attribute("href")
            data['Hotel URL'] = link
        except: data['Hotel URL'] = 'N/A'
        hotel_list.append(data)
    return hotel_list

'''
def fetch_details(driver, url):
    # Visit individual hotel page to fetch coordinates
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "map_trigger_header_pin"))
        )
        latlng_element = driver.find_element(By.ID, "map_trigger_header_pin")
        latlng = latlng_element.get_attribute("data-atlas-latlng")
        latitude, longitude = map(float, latlng.split(',')) if latlng else (None, None)
    except:
        latitude, longitude = None, None

    return latitude, longitude, 'Address not available'

def calculate_distance(hotel_coords, event_coords):
    # Compute distance to event coordinates (in kilometers)
    try:
        return round(geodesic(hotel_coords, event_coords).kilometers, 2)
    except:
        return 'Error'
'''

# GUI
root = tk.Tk()
root.title("Booking Scraper")
root.geometry("500x850")
root.configure(bg="#F3F3F3")
root.resizable(False,False)
#root.iconbitmap("./graphics/icons8.ico") # uncomment if you wish to compile it with an icon

def pick_date(entry):
    top = tk.Toplevel(root)
    top.title("Select date")
    top.grab_set()

    cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(padx=10, pady=10)

    def on_select():
        entry.delete(0, tk.END)
        entry.insert(0, cal.get_date())
        top.destroy()

    tk.Button(top, text="Select", command=on_select).pack(pady=5)

LABEL_FONT = ("Segoe UI", 11)
ENTRY_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 11, "bold")
FG = "#333333"
image = tk.PhotoImage(file="icon.png") # image at the top
label = ttk.Label(image=image)
label.pack(pady=(20,0))
title = tk.Label(
    root,
    text="Booking Scraper",
    font=("Segoe UI", 18, "bold"),
    bg="#F3F3F3",
    fg="#7646ba"
)
title.pack(pady=(20, 10))

container = tk.Frame(root, bg="#FFFFFF", bd=1, relief="flat")
container.pack(pady=10, padx=20, fill="both", expand=False)

def add_label(text):
    return tk.Label(root, text=text, bg=root["bg"], fg=FG, font=LABEL_FONT)

def add_entry():
    return tk.Entry(root, font=ENTRY_FONT, bd=1, relief="solid", highlightthickness=0)

def add_value(from_=0, to=10):
    return tk.Spinbox(
        root,
        from_=from_,
        to=to,
        increment=1,
        relief="solid",
        bd=1,
        highlightthickness=0,
    )

# Inputs
add_label("Number of adults:").pack(pady=(15,0))
entry_adults = add_value(from_=1, to=10)
entry_adults.pack(ipady=3)

add_label("Number of children:").pack(pady=(10,0))
entry_children = add_value(from_=0, to=5)
entry_children.pack(ipady=3)

add_label("Destination:").pack(pady=(10,0))
entry_destination = add_entry(); entry_destination.pack(ipady=3)

add_label("Number of rooms:").pack(pady=(15,0))
entry_rooms = add_value(from_=0, to=10)
entry_rooms.pack(ipady=3)

add_label("Check-in (YYYY-MM-DD):").pack(pady=(10,0))
entry_checkin = add_entry(); entry_checkin.pack(ipady=3)
checkin_frame = tk.Frame(root, bg=root["bg"])
checkin_frame.pack(pady=3)

# Calendar date picker
btn_checkin = tk.Button(
    checkin_frame, text="📅",
    command=lambda: pick_date(entry_checkin),
    bg="#E7E7E7", bd=0, padx=6
)
btn_checkin.pack(padx=5)

add_label("Check-out (YYYY-MM-DD):").pack(pady=(10,0))
entry_checkout = add_entry(); entry_checkout.pack(ipady=3)
checkout_frame = tk.Frame(root, bg=root["bg"])
checkout_frame.pack(pady=3)

btn_checkout = tk.Button(
    checkout_frame, text="📅",
    command=lambda: pick_date(entry_checkout),
    bg="#E7E7E7", bd=0, padx=6
)
btn_checkout.pack(padx=5)

# Start button
start_button = tk.Button(
    root, text="Start", font=BUTTON_FONT,
    bg="#7646ba", fg="white", activebackground="#4d156c",
    activeforeground="white", bd=0, relief="flat", padx=10, pady=6
)
start_button.pack(pady=20)

# Progress bar
status_label = tk.Label(root, text="", bg=root["bg"], fg="#555", font=("Segoe UI", 10))
status_label.pack()
percent_label = tk.Label(root, text="", bg=root["bg"], fg="#777", font=("Segoe UI", 9))
percent_label.pack()
progress = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=260)
progress.pack(pady=10)
progress.pack_forget()


def update_progress(value, status):
    progress["value"] = value
    percent_label.config(text=f"{int(value)}%")
    status_label.config(text=status)
    root.update_idletasks()

# Scraper
def run_scraping_with_progress(adults, children, destination, rooms, checkin, checkout):
    try:
        root.after(0, lambda: update_progress(0, "Starting browser..."))
        driver = create_driver()
        #event_coords = (36.74196135173365, 15.11610252956532)  # Replace with your own event coordinates
        url = f'https://www.booking.com/searchresults.fr.html?ss={destination}&checkin={checkin}&checkout={checkout}&group_adults={adults}&no_rooms={rooms}&group_children={children}'
        driver.get(url)

        root.after(0, lambda: update_progress(20, "Loading results..."))
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="property-card"]'))
        )

        hotels = extract_hotels(driver)
        total = len(hotels)
        root.after(0, lambda: update_progress(40, f"Found {total} hotels"))
        time.sleep(3)

        step = 40
        step_add = 50 / (total if total else 1)
        for idx, h in enumerate(hotels):
            step += step_add
            root.after(0, lambda s=step, i=idx: update_progress(s, f"Extracting hotel {i+1}/{total}"))
            time.sleep(0.05)

        root.after(0, lambda: update_progress(95, "Saving file..."))
        df = pd.DataFrame(hotels)
        filename = f'Hotels - {destination} - {checkin} - {checkout}.xlsx'
        df.to_excel(filename, index=False)

        root.after(0, lambda: update_progress(100, "Done"))
        root.after(0, lambda: messagebox.showinfo("Finished", f"Saved: {filename}"))

    except Exception as e:
        root.after(0, lambda e=e: messagebox.showerror("Error", str(e)))
    finally:
        root.after(2000, lambda: progress.pack_forget())

def on_submit():
    adults = entry_adults.get()
    children = entry_children.get()
    destination = entry_destination.get()
    checkin = entry_checkin.get()
    rooms = entry_rooms.get()
    checkout = entry_checkout.get()

    if not all([adults, children, destination, rooms, checkin, checkout]):
        messagebox.showerror("Error", "Please fill every field.")
        return

    progress["value"] = 0
    percent_label.config(text="")
    status_label.config(text="")
    progress.pack()
    percent_label.pack()
    status_label.pack()

    threading.Thread(
        target=run_scraping_with_progress,
        args=(adults, children, destination, rooms, checkin, checkout),
        daemon=True
    ).start()

start_button.config(command=on_submit)

root.mainloop()
