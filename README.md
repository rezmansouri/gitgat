# GitGat 🍫
a Telegram bot that downloads specific directories in public repositories from GitHub as zip

![image](https://github.com/rezmansouri/gitgat/assets/46050829/06ca32a3-1d9b-49bb-8516-a42c380df41c)


[@gitgatrobot on Telegram](https://t.me/gitgatrobot) - _no guarantee of availability due to free hosting!_
## Introduction
Have you ever wanted to clone only a directory from a GitHub repo and not the whole repo? Well... _GitGat_ is here for it!
_GitGat_ scraps the GitHub repo/directory URL it's given, and extracts its subdirectories' and files' URLs. If the found URL is for a file it is downloaded on its server, otherwise, a local directory representing the directory on GitHub is created to conform with the hierarchy of the repo and starts scrapping that URL. Sounds familiar? This process is basically a DFS (Depth First Search) on a directory implemented recursively.
## Execute GitGat yourself
Either run the `gitgat.py` script or execute it as a worker in a PaaS or VPS.

You will need an API token acquired from [@BotFather](https://t.me/BotFather) for your own Telegram bot.

Assign that token to the `token` variable in the first lines of the `gitgat.py` script:
```
# Access Token of your bot acquired from @BotFather
token = ''
```
## Dependencies
The following Pypi packages were utilized.

`python-telegram-bot v13.12` _GitGat_ was developed using the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) wrapper for the Telegram bot API.

`beautifulsoup4` _GitGat_ uses [beautifulsoup](https://pypi.org/project/beautifulsoup4/) for extracting URLs of files and directories in a GitHub repository.

## How it works
The thrust of this project, is the `helpers.py` script.

This file contains three functions:
+ `crawl(url, dir_name)`:

   A recursive function to crawl the repo/directory `url` and download it completely on the server under a unique `dir_name`.
+ `clear_storage(dir_name)`:

  To remove the downloaded directory and its compressed zip from the server, after it has been sent to the user.
+ `validate_url(url)`:

  A URL validatior to check that only github repo/directory URLs are given as input. It extracts the parent directory name and uses it for the name of the compressed zip file.
## Contributions
_GitGat_ is currently a child and not able to fight the bullies! It is full of vulnerabilities. These are what I have identified so far that can be worked on:
+ Not sure if it is running _asyncly_. Meaning its behavior under concurrent requests is unclear and likely to crash.
+ The process of downloading files locally, zipping them and sending them seems like too much. Probably temp files using the `tempfile` package should be used?

I would be really happy if anyone would like to participate as little as they could.
