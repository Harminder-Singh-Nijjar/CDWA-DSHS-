import time
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    UnexpectedAlertPresentException,
    NoAlertPresentException,
)
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import tkinter.messagebox
import customtkinter
import sys


url = "https://cdmsportal.b2clogin.com/cdmsportal.onmicrosoft.com/b2c_1_r_v4prod_signin/oauth2/v2.0/authorize?client_id=ccfbd7cc-68e2-4ed7-bc54-fa84dff77672&scope=openid%20ccfbd7cc-68e2-4ed7-bc54-fa84dff77672%20profile%20offline_access&redirect_uri=https%3A%2F%2Fdirectmycare.com%2F&client-request-id=5d0cb358-b926-4d4a-9b51-87518f47b191&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.17.0&x-client-OS=&x-client-CPU=&client_info=1&code_challenge=_JJ1vidbIMQCdqFzSxRFeEaOXaOzjU2-pEb-LjqoYqg&code_challenge_method=S256&nonce=eb4c4bec-d7c7-45c5-854d-805b8721a0bb&state=eyJpZCI6ImYwMjBmZjY2LTM2ODgtNGFmMi1iNDk5LWMzZGU2ZmU1NzFkYiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D&ui_locales=ui_locales=en"

# Define user-agents
PC_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36"


def waitUntilVisible(
    browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10
):
    WebDriverWait(browser, time_to_wait).until(
        ec.visibility_of_element_located((by_, selector))
    )


def waitUntilClickable(
    browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10
):
    WebDriverWait(browser, time_to_wait).until(
        ec.element_to_be_clickable((by_, selector))
    )


def browserSetup(
    headless_mode: bool = False, user_agent: str = PC_USER_AGENT
) -> WebDriver:
    # Create Chrome browser
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--start-maximized")
    if headless_mode:
        options.add_argument("--headless")
    chrome_browser_obj = webdriver.Chrome(ChromeDriverManager().install())
    return chrome_browser_obj


def login(browser: WebDriver):
    browser.set_window_size(1024, 600)
    browser.maximize_window()
    email = "EmailAddress"
    password = "Password"
    browser.get(url)
    # Wait to complete loading
    waitUntilVisible(browser, By.XPATH, '//*[@id="email"]', 10)
    emailField = browser.find_element("xpath", '//*[@id="email"]')
    emailField.send_keys(email)
    passwordField = browser.find_element("xpath", '//*[@id="password"]')
    passwordField.send_keys(password)
    browser.find_element("xpath", '//*[@id="next"]').click()
    time.sleep(2)


def punchTime(browser: WebDriver):
    url = "https://directmycare.com/#/user/caregiver/timeshift"
    browser.find_element(
        "xpath",
        "/html/body/app-root/main/app-login/main/section/div/div/div[2]/div[2]/div/div[2]/div/a[1]",
    ).click()
    # Wait to complete loading
    waitUntilVisible(
        browser,
        By.XPATH,
        "//html/body/app-root/main/app-participant/app-cargiverdashboard/section/div[1]/span/button[4]",
        10,
    )
    browser.find_element(
        "xpath",
        "/html/body/app-root/main/app-participant/app-cargiverdashboard/section/div[1]/span/button[4]",
    ).click()
    time.sleep(120)


def main():
    browser = browserSetup(
        False,
    )
    browser.maximize_window()
    login(browser)
    punchTime(browser)


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 420

    def __init__(self):
        super().__init__()

        self.title("CDWA Timesheet Automation")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=20, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(
            0, minsize=10
        )  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(
            8, minsize=20
        )  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(
            11, minsize=10
        )  # empty row with minsize as spacing

        self.switch_1 = customtkinter.CTkSwitch(
            master=self.frame_left,
            text="Dark Mode",
            command=self.change_mode,
            text_font=("Roboto Medium", -10),
        )
        self.switch_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(
            row=0, column=0, columnspan=42, rowspan=6, pady=20, padx=20, sticky="nsew"
        )

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(
            master=self.frame_info,
            text="CDWA Timesheet Automation v0.0.1\n" + "By: Harminder Singh Nijjar",
            height=100,
            text_font=("Roboto Medium", -16),
            fg_color=("white", "gray38"),  # <- custom tuple-color
            justify=tkinter.LEFT,
        )
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        today = time.strftime("%m-%d-%Y")

        self.button_5 = customtkinter.CTkButton(
            master=self.frame_right,
            text=f"Submit timesheet for {today}",
            command=self.submit_time_event,
        )
        self.button_5.grid(
            row=10, column=2, columnspan=1, pady=20, padx=20, sticky="we"
        )

        # set default values
        self.switch_1.select()

    def submit_time_event(self):
        try:
            main()
        except Exception as e:
            print(e)
            messagebox.showerror("Exception", f"{e}")

    def button_event(self):
        print("Button pressed.")

    def change_mode(self):
        if self.switch_1.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
    # url = "https://cdmsportal.b2clogin.com/cdmsportal.onmicrosoft.com/b2c_1_r_v4prod_signin/oauth2/v2.0/authorize?client_id=ccfbd7cc-68e2-4ed7-bc54-fa84dff77672&scope=openid%20ccfbd7cc-68e2-4ed7-bc54-fa84dff77672%20profile%20offline_access&redirect_uri=https%3A%2F%2Fdirectmycare.com%2F&client-request-id=5d0cb358-b926-4d4a-9b51-87518f47b191&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.17.0&x-client-OS=&x-client-CPU=&client_info=1&code_challenge=_JJ1vidbIMQCdqFzSxRFeEaOXaOzjU2-pEb-LjqoYqg&code_challenge_method=S256&nonce=eb4c4bec-d7c7-45c5-854d-805b8721a0bb&state=eyJpZCI6ImYwMjBmZjY2LTM2ODgtNGFmMi1iNDk5LWMzZGU2ZmU1NzFkYiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D&ui_locales=ui_locales=en"
