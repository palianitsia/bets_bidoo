import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from playwright.async_api import async_playwright
import tkinter as tk
from tkinter import messagebox
import asyncio

# Funzione per estrarre i link
def estrai_link():
    output_file = 'Bets.txt'
    open(output_file, 'w').close()
    links = ['https://t.me/s/puntateaste']

    for url in links:
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, 'lxml')

        with open(output_file, 'a') as text_file:
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and 'it.bidoo.com/' in href:
                    clean_link = href.replace('&amp;', '&')
                    text_file.write(clean_link + '\n')

        time.sleep(1)

    print(f"Link estratti e salvati in {output_file}")

# Funzione per il bot Playwright
async def playwright_bot(username, password, links):
    async with async_playwright() as p:
        devices = [
            p.devices["Pixel 5"],
            p.devices["iPhone 12"],
            p.devices["Galaxy S9+"],
            p.devices["iPad (gen 7)"],
            p.devices["Desktop Safari"]
        ]
        
        # Filtrare dispositivi che soddisfano il requisito delle dimensioni 400x800
        mobile_devices = [device for device in devices if device['viewport']['width'] <= 400 and device['viewport']['height'] <= 800]

        if not mobile_devices:
            print("Nessun dispositivo mobile adatto trovato con dimensioni 400x800 o inferiori.")
            return

        device = random.choice(mobile_devices)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(**device)
        page = await context.new_page()

        try:
            await page.goto("https://it.bidoo.com")
            await page.click("#login_btn")
            logging.info("Login button clicked")
            await page.fill("#field_email", username)
            await page.fill("#password", password)
            await page.click('button.btlogin:nth-child(1)')
            await page.wait_for_timeout(2000)
            
            for link in links:
                await page.goto(link)
                logging.info(f"Opened link: {link}")
                await page.wait_for_timeout(2000)  # Pausa
        finally:
            await browser.close()

# Funzione per avviare il processo
def avvia_processo():
    username = entry_username.get()
    password = entry_password.get()
    manual_link = entry_manual_link.get()
    usa_lista = var_usa_lista.get()

    links = []

    if manual_link:  # Se l'utente ha inserito un link manuale, usalo
        links.append(manual_link)
    else:
        # Estrazione dei link
        estrai_link()

        # Leggi i link dal file 'Bets.txt'
        with open('Bets.txt', 'r') as file:
            links.extend([line.strip() for line in file.readlines()])

    if usa_lista:
        with open('acc.txt', 'r') as file:
            accounts = file.readlines()
            for account in accounts:
                user, pwd = account.strip().split(',')
                asyncio.run(playwright_bot(user, pwd, links))
    else:
        asyncio.run(playwright_bot(username, password, links))

# Creazione della GUI
root = tk.Tk()
root.title("Bot Telegram")

tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show='*')
entry_password.pack()

tk.Label(root, text="Link manuale (opzionale)").pack()
entry_manual_link = tk.Entry(root)
entry_manual_link.pack()

var_usa_lista = tk.BooleanVar()
tk.Checkbutton(root, text="Usare acc da lista", variable=var_usa_lista).pack()

tk.Button(root, text="Avvia", command=avvia_processo).pack()

root.mainloop()
