## Overview 

This was my first personal project I began shortly after taking my first programming course, so the code isn't the greatest. 

It is a standard typing speed test that will measure typing metrics such as your words per minute and typing accuracy. As most basic typing tests go, you will have a set time, 30 seconds in this case, to correctly type a collection of random words. 

Despite being a pretty simple project, I think the GUI and UX is pretty nice for being made with a relatively primitive GUI library. I tried to copy some of [MonkeyType's](https://monkeytype.com/) UI/UX such as indicators when not only certain characters are incorrect, but if too many characters were typed for the current word. 

### Examples

![Incorrect characters example](img/incorrect-chars-ex.png)

<p align="center"><em>Getting characters incorrect.</em></p>

![Example of too many characters for a word](img/too-long-ex.png)

<p align="center"><em>Typing too many characters for a word.</em></p>

![Example of using the app](img/demo.gif)

<p align="center"><em>App demo.</em></p>

## Usage

Simply start typing to begin the test. Press the `shift` key at any time to restart the test and shuffle the words. After the test is over, metrics about your test will display. 
## Installation

Clone the repo:

```
git clone https://github.com/defcarlito/WPM-Typing-Test
```

Install the only dependency:

```
pip install pyside6
```

Run the app:

```
python3 main.py
```
