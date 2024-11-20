> [!NOTE]  
> This script lacks a lot of customisation.

<br>

# Wraith vault custom reward

This script will allow you to modify the request sent to the gd servers (when using the wraith vault) to modify the reward to your liking

# Installation

You'll need to download a tool known as [mitmproxy](https://mitmproxy.org/) and [python](https://www.python.org/) (at least version 3).

This dosen't require any other dependencies! (todo: test this statement)

# How to use

> [!NOTE]  
> Do note that for **EVERY** tried code tried in the wraith vault, this script will **ALWAYS** modify the request's response

## Running the script

Run `start.bat` (You will need to run it as an administrator *(for Windows at least)*)

**Or**:
- Open **CMD**
- Go to the directory where the python script is located (using `cd`)
- Run:

[comment]: <> (Using `python` syntaxing because uhhh colors)
```cmd
mitmdump --mode transparent -s main.py
```

Or use it the interactive version of mitmproxy:

```cmd
mitmproxy --mode transparent -s main.py
```

## Changing the reward

You can easily change the reward's content. At the top of the file you can see:

```py
REWARD_ID = None # You will need to set a unique ID every time
ITEM_ID = None
NUM_OF_ITEMS = None
```

### Examples:

So if for example, we want to be **rewarded 3** orbs we will do:

```py
REWARD_ID = 1000 # This ID is just an example, it's set to 1000 so we are sure it won't ever conflict with the 'official' rewards
ITEM_ID = Items.Obtainables.orb
NUM_OF_ITEMS = 3
```

But if we instead **want 1 golden key**, we can do it like so:

```py
REWARD_ID = 1001 # This ID is just an example, it's set to 1000 so we are sure it won't ever conflict with the 'official' rewards
ITEM_ID = Items.Keys.golden_key
NUM_OF_ITEMS = 1
```
