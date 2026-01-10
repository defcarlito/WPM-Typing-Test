## Overview 

This was my first personal project I began shortly after taking my first programming course, so the code isn't the greatest. 

It is a standard typing speed test that will measure typing metrics such as your words per minute and typing accuracy. As most basic typing tests go, you will have a set time, 30 seconds in this case, to correctly type a collection of random words. 

Despite being a pretty simple project, I think the GUI and UX is pretty nice for being made with a relatively primitive GUI library. I tried to copy some of [MonkeyType's](https://monkeytype.com/) UI/UX such as indicators when not only certain characters are incorrect, but if too many characters were typed for the current word. 

### Examples

<p align="center">
<img src="img/incorrect-chars-ex.png" alt="Incorrect characters example" />
<br />
<em>Getting characters incorrect.</em>
</p>

<p align="center">
<img src="img/too-long-ex.png" alt="Too many characters example" />
<br />
<em>Typing too many characters for a word.</em>
</p>

<p align="center">
  <img src="img/demo.gif" alt="App demo" />
  <br />
  <em>App demo.</em>
</p>

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
