# DAAV - Detection of Android Aplication Vulnerabilities

This is my Master Degree's on Open Source Software prototype.
I's a vulnerability analysis tool over Android applications that is available through a website, which differs from other tools with similar purpose, because it includes several vulnerabilities detection tools and creates a single normalized report to expose software vulnerabilities and categorize them for user interpretation, adding guides to solve those security flaws over each vulnerability.
This solution is the result of a study over existent vulnerabilities detection tools, malicious software attack methods and software security flaws categorization to propose guides that could solve each of those vulnerabilities found.

It started as a fork of AppSentinel and become something quite different.

## Still under development

There is a lot of things to be done in DAAV to become a good tool to detect vulnerabilities.
there is no demo or instructions to install, you can use the code on a Visual Studio Code and "npm run serve"

## How to use DAAV

The idea here is to join other tools that check for Android vulnerabilities and use them as plugins into DAAV, gather their information and normalize a single report to the user categorized into OWASP Mobile Top Ten.

Install both Pythons (2 and 3)
https://www.python.org/downloads/
(Both versions over Windows:https://spapas.github.io/2017/12/20/python-2-3-windows/)

Install requirement: FLASK
pip install -U Flask
pip install -U flask-cors

Install MySQL Server
https://dev.mysql.com/downloads/installer/

Install requirement: PyMySQL
pip install PyMySQL
py -2 -m pip install pymysql
(2x - using pip on Python 2 and 3)

Install requirement: flasgger
pip install -U setuptools
pip install flasgger

Install requirement: Python Requests Library
pip install requests
pip install cryptography

Install requirement: Python tqdm
pip install tqdm

Install requirement: Python JWT Authentication
pip install PyJWT

Install Vue Cli
npm install -g @vue/cli

For Visual Studio Code:
File » Preferences » Settings » Extensions » JSON » Edit settings.JSON
 "python.linting.pylintArgs": ["--load-plugins", "pylint_flask_sqlalchemy"],

Install MySQL for Visual Studio Code
https://marketplace.visualstudio.com/items?itemName=formulahendry.vscode-mysql

Install MySQL Server and create users (check config.ini)

Change config.ini the pythoncmd for python2 and python3 of your machine (py -2 / py -3)

For the first time, over webfrontend directory, open powershell and: npm i

## Built With

* [VueJs](https://vuejs.org/) - Javascript framework
* [VueUI](https://vueui.github.io/) - To start the project
* [Visual Studio Code](https://code.visualstudio.com/) - To code
* [Sourcetree](https://www.sourcetreeapp.com/) - Version control
* [Python](https://www.python.org/) - API
* [MySQL](https://www.mysql.com/) - Database

## Authors

**Raphael Candello**

## Open Source

This project is completely open-source, fell free to use the code.
