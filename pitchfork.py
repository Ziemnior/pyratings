from bs4 import BeautifulSoup as Soup
from tkinter import *
from PIL import Image, ImageTk
import io
import urllib.parse
import webbrowser

mainWindow = Tk()
mainWindow.title("Latest Pitchfork reviews")
mainWindow.resizable(0, 0)

website = "http://pitchfork.com/reviews/albums/"
request_website = urllib.request.Request(url=website, data=None, headers={
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'})
fetch_website = urllib.request.urlopen(request_website).read()
open_website = Soup(fetch_website, 'html.parser')

results = []
images = []
circle_image = []
BLACK_CIRCLE = "images/p4k_circle_black.png"
RED_CIRCLE = "images/p4k_circle_red.png"


def replace_date():
    global date
    date = get_date

    day_year = get_date[5:]
    day = day_year[0:2]
    year = day_year[3:]
    s='.'

    if date.find('January') != -1:
        month = '01'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('Febuary') != -1:
        month = '02'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('March') != -1:
        month = '03'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('April') != -1:
        month = '04'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('May') != -1:
        month = '05'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('June') != -1:
        month = '06'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('July') != -1:
        month = '07'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('August') != -1:
        month = '08'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('September') != -1:
        month = '09'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('October') != -1:
        month = '10'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('November') != -1:
        month = '11'
        date_ = (day, month, year)
        date = s.join(date_)
    elif date.find('December') != -1:
        month = '12'
        date_ = (day, month, year)
        date = s.join(date_)
    return date


for i in open_website.find_all('a', {'class': 'album-link'}, href=True):
    temp = "http://pitchfork.com" + i['href']
    results.append(temp)

latest_review = results[0]
print(latest_review)

for i in range(0, 8):
    review = results[i]
    request_website = urllib.request.Request(url=review, data=None, headers={
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'})
    fetch_website = urllib.request.urlopen(request_website).read()
    open_website = Soup(fetch_website, 'html.parser')
    get_rating = open_website.find(name="span", attrs={'class': 'score'}).text
    get_album = open_website.find(name="h1", attrs={'class': 'review-title'}).text
    get_artist = open_website.find(name="h2", attrs={'class': 'artists'}).text
    get_cover_url = open_website.find('img')['src']
    get_author = open_website.find(name="a", attrs={'class': 'display-name'}).text
    get_date = open_website.find(name="span", attrs={'class': 'pub-date'}).text

    bnm = open_website.find("p", class_="bnm-txt")
    if bnm != None:
        circle = ImageTk.PhotoImage(Image.open(RED_CIRCLE))
        circle_image.append(circle)
        rating = Label(font=("Walfork", 12, "bold"), fg="#FF3530", text=get_rating, image=circle, compound=CENTER)
    else:
        circle = ImageTk.PhotoImage(Image.open(BLACK_CIRCLE))
        circle_image.append(circle)
        rating = Label(font=("Walfork", 12, "bold"), text=get_rating, image=circle, compound=CENTER)

    artist_and_album = Label(font=("Walfork", 12, "bold"), text=get_artist + ' - ' + get_album, cursor="hand2")


    def open_in_browser(review):
        artist_and_album.bind('<Button-1>', lambda event: webbrowser.open(review, 0, True))

    open_in_browser(review)
    artist_and_album.bind('<Enter>', open_in_browser)

    author = Label(font=("Walfork", 8, "bold"), text=get_author)
    replace_date()
    date = Label(font=("Walfork", 8), fg="#B3B3B3", text=date)

    open_cover = urllib.request.urlopen(get_cover_url).read()
    opened_cover = Image.open(io.BytesIO(open_cover))
    resized_cover = opened_cover.resize((100, 100), Image.ANTIALIAS)
    final_cover = ImageTk.PhotoImage(resized_cover)
    image_cover = Label(mainWindow, image=final_cover, borderwidth=1, bg='black', fg='white')
    images.append(final_cover)

    image_cover.grid(row=i, column=0, sticky=W)
    artist_and_album.grid(row=i, column=1, sticky=W + N, pady=20)
    rating.grid(row=i, column=2, sticky=W + N, pady=20, padx=10)
    author.grid(row=i, column=1, sticky=W + N, pady=40, ipady=5)
    date.grid(row=i, column=1, sticky=W + N, pady=40, padx=150, ipady=5)

mainWindow.iconbitmap(r'images/icon.ico')
mainWindow.mainloop()