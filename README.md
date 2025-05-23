> [!NOTE]  
> This script lacks a lot of customisation.

> [!IMPORTANT]
> If you do not want to keep the obtained custom rewards, make sure to follow whats in [backup.md](./backup.md)

<br>

# Wraith vault custom reward

This script will allow you to modify the request sent to the gd servers (when using the wraith vault) to modify the reward to your liking.

# Installation

You'll need to download a tool known as [mitmproxy](https://mitmproxy.org/). Alternativaly, you can download it by running `pip install mitmproxy` if you have [python](https://www.python.org/) installed.
This dosen't require any other dependencies !

# How to use

> [!NOTE]
> Do note that for **EVERY** tried code tried in the wraith vault, this script will **ALWAYS** modify the request's response.

## Running the script

Run `start.bat` (You will need to run it as an administrator *(for Windows at least)*)

**Or**:
- Open **CMD** as **administrator**
- Go to the directory where the python script is located (using `cd`)
- Run:

[comment]: <> (Using `python` syntaxing because uhhh colors)
```cmd
mitmdump --mode local -s main.py
```

Or use it the interactive version of mitmproxy :

```cmd
mitmproxy --mode local -s main.py
```

> [!NOTE]  
> When running this, every requests made using **https** won't go through. For example if you are running this script but want to access discord in the meantime, you will need to close the `mitmproxy` instance)

> [!TIP]
> Every time you change the reward, you won't need to execute the `mitmproxy` command again. `mitmproxy` updates it's modules every a new **saved change** has been made.
> *(this script is a `mitmproxy module`)*

## Changing the reward

You can easily change the reward's content. At the top of the file you can see :

```py
REWARD_ID = None # You will need to set a unique ID every time
ITEM_ID = None
NUM_OF_ITEMS = None
```

For it to work each time, you will need to change the `REWARD_ID` var. Try to keep it above a huge number so that it won't **conflict with robtop's rewards**

### Examples:

So if for example, we want to be **rewarded 3** orbs we will do :

```py
REWARD_ID = 1000 # This ID is just an example, it's set to 1000 so we are sure it won't ever conflict with the 'official' rewards
ITEM_ID = Items.Obtainables.orb
NUM_OF_ITEMS = 3
```

But if we instead **want 1 golden key**, we can do it like so :

```py
REWARD_ID = 1001 # This ID is just an example, it's set to 1001 so we are sure it won't ever conflict with the 'official' rewards
ITEM_ID = Items.Keys.golden_key
NUM_OF_ITEMS = 1
```
