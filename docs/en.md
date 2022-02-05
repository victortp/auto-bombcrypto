# 💣 Auto BOMBCRYPTO

![GitHub repo size](https://img.shields.io/github/repo-size/victortp/auto-bombcrypto?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/victortp/auto-bombcrypto?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/victortp/auto-bombcrypto?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/victortp/auto-bombcrypto?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/victortp/auto-bombcrypto?style=for-the-badge)

<img src="https://github.com/victortp/auto-bombcrypto/blob/main/docs/logo.png" alt="Auto BOMBCRYPTO">

> Auto BOMBCRYPTO is an automation tool for the game [Bombcrypto](https://app.bombcrypto.io/)

## 💎 Features

- Login/reconnect
- Select the heroes to work (all at at once/all that have green energy bar)
- Refresh heroes position in the map
- Log chest's Bcoin amount
- Support multiple accounts

## 💻 Prerequisites

Before beginning, make sure that you have met the following requirements:

- You have the latest `Python` version installed ([download](https://www.python.org/downloads/))
- You know how to use the `command prompt/terminal`
- Installed the following packages if you use unix system:

```
sudo apt install scrot python3-gi python3-gi gir1.2-wnck-3.0 python3-tk python3-dev -y
```

## 🚀 Installing Auto BOMBCRYPTO

To install Auto BOMBCRYPTO, follow the steps below:

- Open the project folder in the command prompt/terminal

```
cd path/to/project-folder/
```

- Install the dependencies

```
pip install -r requirements.txt
```

## ☕ Using Auto BOMBCRYPTO

To use Auto BOMBCRYPTO, follow the steps below:

- Open [Bombcrypto website](https://app.bombcrypto.io/)
- Open the project folder in the command prompt/terminal

```
cd path/to/project-folder/
```

- Run the project

```
python main.py
```

- As it is an image based tool, keep the browser window visible at all times
- To stop it, just press `ctrl + c` in the command prompt/terminal

## 🤖 Multiple accounts

To use multiple accounts, open the browsers, go to the bombcrypto page and leave the metamask authenticated.
The tool will identify the presence of multiple accounts.

## ⚙️ Tweaks

You can change the tool's behavior by changing the following variables in the `main.py` file:

> ⚠️ **Changing these variables may break the tool**

```python
# ACTIONS COOLDOWN IN MINUTES
SEND_HEROES_TO_WORK = 10
REFRESH_HEROES_POSITION = 3
LOG_BCOIN = 30
CHECK_CONNECTION = 1/60

# MISCELLANEOUS
SEND_ALL_HEROES_TO_WORK = False  # True = yes | False = no
SAVE_LOG_TO_FILE = True  # True = yes | False = no
RANDOMIZE_MOUSE_MOVEMENT = True  # True = yes | False = no
LOGIN_STEP_ATTEMPTS = 20 # Number of attempts to complete each step of the login proccess
```
