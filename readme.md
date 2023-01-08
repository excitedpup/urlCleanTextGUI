# Url Into Text Program
Rowan Fall 2022 student NLP work

Author: Danielle Whitmarsh

Used ca_text_clean.py example from my professor (console application) and added GUI (graphical user interface).

Tkinter was used to make gui.

Program takes URL input from input box.

Retrieves html from url and cleans text when 'Clean Up' button is pressed.

    In method, many cleanings are done like removing punctuation, contractions, and noise.
    The result is displayed in scroll text box.

Outputs result of clean up to text file 'Documents/CleanTextFiles/clean_text.txt' when ‘Save’ button is pressed.

'Quit' button exits out of program.

## Setup & Installation
Ways to run program:

1. Through the Executables
2. Through GitHub clone:

```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

## Running The App

```bash
python url_into_text.py
```

Console application requires arguments to launch:

    1. Input argument  -i {"SOME_URL"}
    2. Output argument -o "clean_text.txt"

## Viewing The App

The program window should display.