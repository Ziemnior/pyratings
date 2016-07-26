from bs4 import BeautifulSoup as Soup
from tkinter import *
from PIL import Image, ImageTk
import io
import urllib.request
import webbrowser


website = "http://www.porcys.com/review/"
open_website = Soup(urllib.request.urlopen(website), 'html.parser')
reviews = open_website.find(name="section", attrs={'class': 'slider-content review'}).ul


results = []


for a in reviews(href=True):
    temp = "http://www.porcys.com" + a['href']
    results.append(temp)

global latest_review_porcys
latest_review_porcys = results[0]
print(latest_review_porcys)


mainWindow = Tk()
mainWindow.title("Latest Porcys reviews")
mainWindow.resizable(0, 0)

images = []

def replace_date():
    global date
    date = get_date.text
    if date.find('stycznia') != -1:
        date = date.replace(' stycznia ', '.01.')
    elif date.find('lutego') != -1:
        date = date.replace(' lutego ', '.02.')
    elif date.find('marca') != -1:
        date = date.replace(' marca ', '.03.')
    elif date.find('kwietnia') != -1:
        date = date.replace(' kwietnia ', '.04.')
    elif date.find('maja') != -1:
        date = date.replace(' maja ', '.05.')
    elif date.find('czerwca') != -1:
        date = date.replace(' czerwca ', '.06.')
    elif date.find('lipca') != -1:
        date = date.replace(' lipca ', '.07.')
    elif date.find('sierpnia') != -1:
        date = date.replace(' sierpnia ', '.08.')
    elif date.find('września') != -1:
        date = date.replace(' września ', '.09.')
    elif date.find('października') != -1:
        date = date.replace(' października ', '.10.')
    elif date.find('listopada') != -1:
        date = date.replace(' listopada ', '.11.')
    elif date.find('grudnia') != -1:
        date = date.replace(' grudnia ', '.12.')


for i in range(0, 8):
    review = results[i]
    open_review = Soup(urllib.request.urlopen(review), 'html.parser')
    get_rating = open_review.find(name="span", attrs={'class': 'rating'})
    get_album = open_review.find(name="div", attrs={'class': 'wrapper'}).i
    get_artist = open_review.find(name="div", attrs={'class': 'wrapper'}).h2
    get_cover_url = open_review.find(name="img", attrs={'class': 'cover'})
    for tag in open_review.find_all('i'):
        tag.replaceWith(' ')
    cover = "http://www.porcys.com" + get_cover_url['src']
    get_author = open_review.find(name="span", attrs={'class': 'author'})
    get_date = open_review.find(name="div", attrs={'class': 'db-date'})

    # replace words in date with numbers
    replace_date()

    # artist and album to label
    artist_and_album = Label(font=("OpenSansRegularItalic", 12, "bold"), text=get_artist.text + '- ' + get_album.text,
                             cursor="hand2")


    def open_in_browser(review: object) -> object:
        artist_and_album.bind('<Button-1>', lambda event:webbrowser.open(review, 0, True))
    open_in_browser(review)


    artist_and_album.bind('<Enter>', open_in_browser)

    # rating to label
    rating = Label(font=("OpenSansBold", 12, "bold"), fg='#00d0cd', text=get_rating.text)

    # delete newlines form get_author
    author = get_author.text
    author = author.replace('\n', '')
    author = ' '.join(author.split())

    # author to label
    author = Label(font=("OpenSansBold", 8, "bold"), text=author)

    # date to label
    date = Label(font=("OpenSansRegular", 8), fg='#939598', text=date)

    # resize cover
    open_cover = urllib.request.urlopen(cover).read()
    opened_cover = Image.open(io.BytesIO(open_cover))
    resized_cover = opened_cover.resize((100, 100), Image.ANTIALIAS)
    final_cover = ImageTk.PhotoImage(resized_cover)
    image_cover = Label(mainWindow, image=final_cover, borderwidth=1, bg='black', fg='white')
    images.append(final_cover)

    # put labels in the grid
    image_cover.grid(row=i, column=0, sticky=W)
    artist_and_album.grid(row=i, column=1, sticky=W + N, pady=20)
    rating.grid(row=i, column=2, sticky=W + N, pady=20, padx=10)
    author.grid(row=i, column=1, sticky=W + N, pady=40, ipady=5)
    date.grid(row=i, column=1, sticky=W + N, pady=40, padx=150, ipady=5)


mainWindow.iconbitmap(r'images/icon.ico')
mainWindow.mainloop()
