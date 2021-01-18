# sakura-patcher
Unoffical Application to patch your sakura games

I created this for myself after buying the budle on steam I noticed that there are patches availavbel for some games.
Because it's a pain in the ass to patch all games manually I wanted to make a application to do it for me and possibly for you.

All content is provided by the official Winged Cloud Patreon [https://www.patreon.com/wingedcloud](https://www.patreon.com/wingedcloud)  
I don't own any game content!

## Getting started

Install the latest version of [Python](https://www.python.org/downloads/). After installing Python open a Command Prompt or Terminal.  
Install the dependencies:  

    python -m pip install -r requirements.txt

Now you can run the program like this:

    python sakura-patcher.py [Your Path to your Steam Libary here]

In my case I have to do it like this:

    python sakura-patcher.py K://

The program will understand that your games are in the Steam folder at the following path: .../Steam/steamapps/common/  
Now just run the command above and wait until it's finished. The process might take a while because some of the files are quite large (~150MB). If you wanna stop the programm at any time press ctrl + C.

## !!Also all your old files will get overwritten!!

So if you wanna just try it out then manually backup your old .rpa files.  
.../Steam/steamapps/common/Sakura .../game/*.rpa