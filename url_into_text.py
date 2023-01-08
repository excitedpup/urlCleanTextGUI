"""
Danielle Whitmarsh
Made 10-09-2022
Added clean text display 01-06-2023

console application requires arguments to launch:
1. Input argument  -i {URL allowed by robot.txt}
2. Output argument -o "Documents/CleanTextFiles/clean_text.txt"
"""

# Import all libraries
import re
import unicodedata
from tkinter import messagebox
import inflect
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import urllib3
import sys
import getopt
from tkinter import *
from tkinter import scrolledtext
import os

# Define global variables
outfile = ''
words = []
url = ''


# Define functions

# Using cleaning tools as directed by my Rowan NLP class.
def strip_html(text):
    """ Use BeautifulSoup to get text from html """
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_between_square_brackets(text):
    # clean brackets
    return re.sub('\[[^]]*\]', '', text)


def denoise_text(text):
    """ denoise text """
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text


def remove_non_ascii(arg_words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in arg_words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)

    return new_words


def to_lowercase(arg_words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in arg_words:
        new_word = word.lower()
        new_words.append(new_word)

    return new_words


def remove_punctuation(arg_words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in arg_words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)

    return new_words


def replace_numbers(arg_words):
    """Replace all integer occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in arg_words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)

    return new_words


def remove_stopwords(arg_words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in arg_words:
        if word not in stopwords.words('english'):
            new_words.append(word)

    return new_words


def stem_words(arg_words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in arg_words:
        stem = stemmer.stem(word)
        stems.append(stem)

    return stems


def lemmatize_verbs(arg_words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in arg_words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)

    return lemmas


def normalize(arg_words):
    arg_words = remove_non_ascii(arg_words)
    arg_words = to_lowercase(arg_words)
    arg_words = remove_punctuation(arg_words)
    arg_words = replace_numbers(arg_words)
    arg_words = remove_stopwords(arg_words)

    return arg_words


# Main Function
def main():
    # Set global variables
    global url
    global outfile
    global words

    # Create gui window, size, title, and background color
    root = Tk()
    root.minsize(680, 840)
    root.maxsize(680, 840)
    root.configure(bg='honeydew')
    root.title('Url into Text')

    # Set entry global variable
    global url_var
    url_var = StringVar()

    # Create clean up button and assign clean up onclick method to it
    start_button = Button(
        root,
        text="Clean Up",
        width=10,
        height=2,
        relief=RAISED,
        command=clean_up_on_click
    )
    start_button.place(relx=0.2, rely=0.9, anchor=CENTER)

    # Create save button and assign save onclick method to it
    save_button = Button(
        root,
        text="Save",
        width=10,
        height=2,
        relief=RAISED,
        command=save_on_click
    )
    save_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    # Create exit button and assign quit method to it
    exit_button = Button(
        root,
        text="Quit",
        width=10,
        height=2,
        relief=RAISED,
        command=lambda: root.quit()
    )
    exit_button.place(relx=0.8, rely=0.9, anchor=CENTER)

    # Creates Enter URL label
    url_label = Label(root,
                      text="Enter URL",
                      bg='honeydew')
    url_label.place(relx=0.5, rely=0.05, width=500, height=40, anchor=CENTER)

    # Creates entry text box and assigns input to url_var
    url_entry = Entry(
        root,
        textvariable=url_var,
        font=('calibre', 20, 'normal'))
    url_entry.place(relx=0.5, rely=0.1, width=500, height=40, anchor=CENTER)

    # Creates scroll box for output
    global url_output
    url_output = scrolledtext.ScrolledText(
        root,
        wrap=WORD,
        font=("Times New Roman", 15),
        state="disabled"
    )
    url_output.place(relx=0.5, rely=0.5, width=500, height=550, anchor=CENTER)

    # Creates label for save file
    global saved_label
    saved_label = Label(
        root,
        text='',
        font=("Times New Roman", 15),
        bg='honeydew'
    )
    saved_label.place(relx=0.5, rely=0.95, anchor=CENTER)

    # Runs window
    root.mainloop()


# Checks if input is entered and then runs program on inputted url otherwise sends error message
def clean_up_on_click():
    global words
    global url
    global url_var

    if len(url_var.get()) == 0:
        messagebox.showerror('Python Error', 'Error: No url entered!')
    else:
        url = url_var.get()
        words = run(url)
        # Displays web scraped words
        url_output.configure(state="normal")
        url_output.delete(1.0, END)
        url_output.insert(INSERT, words)
        url_output.configure(state="disabled")
    # print(len(url_var.get()))
    # print(words)
    return words


# Web scrapes then cleans scraped data
def run(argv):
    global url
    global words
    global outfile

    url = argv

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["iurl=", "ofile="])
    except getopt.GetoptError:
        print('ca_text_clean -i <url>, -o <file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('ca_text_clean -i <url>, -o <file>')
            sys.exit()
        elif opt in ("-i", "--iurl"):
            url = arg
        elif opt in ("-o", "--ofile"):
            outfile = arg

    # get the page
    print("url=", url)
    http = urllib3.PoolManager()

    # Catch error if request is unreachable
    try:
        page = http.request('GET', url)
        # cleaning data
        sample = denoise_text(page.data)
        words = nltk.word_tokenize(sample)
        words = normalize(words)
        # print(words)

    except urllib3.exceptions.MaxRetryError:
        messagebox.showerror('Python Error', 'Error: Unable to get local issuer certificate!')

    return words


# Runs save method with what is ever assigned to words
def save_on_click():
    global words
    save(words)
    saved_label.config(text='Saved to Documents/CleanTextFiles/clean_text.txt')
    # print(words)


def save(arg_words):
    global outfile
    # Gets os path
    cwd = os.path.abspath(os.getcwd())

    if outfile == '':
        outfile = 'Documents/CleanTextFiles/clean_text.txt'

    # Adds txt file to same place as program
    outfile = os.path.join(cwd, outfile)

    # save clean words to file
    f = open(outfile, 'w')
    for wd in arg_words:
        f.write(wd + '\n')


# Start the script
if __name__ == '__main__':
    main()
