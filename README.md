# 🏨 Booking Scraper

This Python project uses **Selenium** and **Tkinter** to automatically extract hotel data from **Booking.com**. It features a graphical interface to define search parameters (destination, dates), then stores the result in an Excel file. Ideal for comparing hotels around an event location such as a wedding, festival, or conference.

## EDITS MADE
- **Enchanced GUI** fully ready to be compiled as an executable file with new added progress bar to inform about program status.
- **Commented out the Adress, GPS coordinates, Star rating, Distance from a fixed location functions** Due to their problematic behaviour and to provide faster compilation - ***If you wish to still use these functions simply uncomment them.***
- **New Inputs** such as: Number. of adults, children, rooms.
- **Calendar Date Picker** to simplify the process of Check-in and Check-out date input.
- **Re-wrote scroll_until_all_hotels_loaded** to ensure every hotel from your Destination is loaded.

## ✨ Features

- **User-friendly GUI** with `Tkinter`
- **Automated hotel data extraction**:
  - Hotel name
  - Star rating ***# commented out #***
  - Price
  - Review score
  - Booking.com link
  - Address and GPS coordinates ***# commented out #***
  - Distance from a fixed location ***# commented out #***
- **Distance calculation** using `geopy` ***# commented out #***
- **Excel export** with `pandas` and `openpyxl`


## 🗂 Project Structure

```bash
booking_scraper/
├── hotels_booking.py         # Main script
├── chromedriver/             # Folder containing the ChromeDriver
├── graphics/                 # Folder containing the UI graphics
├── README.md                 # English version
├── requirements.txt          # Required libraries
├── icon.png                  # Image at the top of GUI
````


## ✅ Requirements

* Python 3.12.4
* Google Chrome installed
* ChromeDriver ([https://chromedriver.chromium.org/](https://chromedriver.chromium.org/))
* Python libraries:

  * `selenium`
  * `webdriver_manager`
  * `pandas`
  * `geopy`
  * `openpyxl`
  * `tkcalendar`


## ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/8hills/Booking_scraper.git
   ```
   
   ```bash
   cd Booking_scraper
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `chromedriver` is correctly located and executable in the expected folder.


## 🚀 How to Use

1. Run the script:

   ```bash
   python hotels_booking.py
   ```

2. In the GUI window:
   * Enter number of **adults**
   * Enter number of **children (i.e people in the span of age 0-17)**
   * Enter your **destination**
   * Enter number of **rooms**
   * Select your **check-in** and **check-out** dates (`YYYY-MM-DD`)
   * Click **Start**

4. Once scraping is complete, an Excel file will be generated with the results:

   ```
   Hotels - <Destination> - <Checkin> - <Checkout>.xlsx
   ```

## 🧠 Technical Overview

### Main Functions:

* `extract_hotels(driver)`: Extracts the main hotel information from the Booking results page.
* `fetch_details(driver, hotel_link)`: Gathers additional details such as address, latitude, and longitude.
* `calculate_distance(hotel_coords, event_coords)`: Computes distance in kilometers between each hotel and a fixed reference point.
* `run_scraping(destination, checkin, checkout)`: Orchestrates the scraping process and writes to Excel.
* `on_submit()`: GUI callback triggered when the user clicks the scraping button.


## 📄 Sample Excel Output

| Hotel Name   | Price (Currency based on Booking's link location) | Score (/10) | Booking Link |
| ------------ | ------------------------------------------------- | ----------- | ------------ |
| Hotel Sample |                       142.00                      | 8.2         | https\://... |


## ⚠️ Disclaimer

This script is for **educational purposes only**. Scraping Booking.com may violate their terms of service. Use responsibly and respect website rules.


## 👤 Author

Developed by [ALeterouin](https://github.com/ALeterouin)
Edited by [8hills](https://github.com/8hills)

Free to use and modify

<<<<<<< HEAD:ReadME
=======
Cela devrait fournir toutes les informations nécessaires aux utilisateurs pour comprendre, installer et exécuter votre projet !
>>>>>>> 0983c147ee08a4ed2b219d6fdd7f40e34f660ba9:README.md
