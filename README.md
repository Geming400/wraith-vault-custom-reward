# Wraith vault custom reward

This script will allow you to modify the request sent to the gd servers (when using the wraith vault) to modify the reward to your liking

# Installation

You'll need to download a tool known as [mitmproxy](https://mitmproxy.org/) and [python](https://www.python.org/) (at least version 3).
This dosen't require any dependency! (todo: test this statement)

# How to use

Run `start.bat` (You will need to run it as an administrator *(for Windows at least)*)

**Or**:
- Open **CMD**
- Go to the directory where the python script is located
- Run:

[comment]: <> (Using `python` syntaxing because uhhh colors)
```cmd
mitmdump --showhost --mode transparent -s main.py
```

Or use it the interactive version of mitmproxy:

```cmd
mitmproxy --showhost --mode transparent -s main.py
```
