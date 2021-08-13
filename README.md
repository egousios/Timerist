<div style="margin-left: 50px">
<h1>Timerist (In Construction 👷 🚧)</h1>
<img alt="Stars" src="https://img.shields.io/badge/build-passing-brightgreen">
<img alt="Issues" src="https://img.shields.io/github/issues-raw/DaEliteCoder/Timerist">
<img alt="Language" src="https://img.shields.io/badge/language-python-blue.svg">
<img alt="Language" src="https://img.shields.io/badge/language-golang-red.svg">
<img alt="Framework" src="https://img.shields.io/badge/framework-PyQt5-blue.svg">
  
<h4>An application that will help students organize their day at school :)</h4>
</div>
<br>


Table of contents
=================
<!--ts-->
   * [Table of contents](#Table-of-contents)
   * [Screenshots](#Screenshots)
   * [Running the Application from Source](#Running-the-Application-from-Source)
   * [Code Insight](#Code-Insight)
   * [Settings API](#Settings-API)
   * [Development Checklist](#Development-Checklist)
   * [Notices](#Notices)
   * [License](#License)
<!--te-->

Screenshots
===
#### light and dark theme mode:
<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/main_light.png">
<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/main_dark.png">
<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/editor_light.png">
<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/editor_dark.png">
<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/add_todo_light.png">
<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/view_todo_light.png">

Running the Application from Source
===
### Running from source (Windows):
Make sure that you have 'pip' installed on your system, and that you have added it to your Python path.
If you have completed the step above, you may move on to completing the steps below.
Open up your terminal, and type or paste in the following:
1. `git clone "https://github.com/DaEliteCoder/Timerist.git"`
2. `cd Timerist && cd src && pip install -r requirements.txt && cd auth && python -u Auth.py`
---
#### Optional: To check if the dependencies were installed properly, type or paste in the following in your terminal: 
`pip freeze`
### Running from source (MacOS / Linux):
Make sure that you have 'pip' installed on your system, and that you have added it to your Python path.
If you have completed the step above, you may move on to completing the steps below. Remember, Python version 2 is pre-installed on your operating system, so you will have to say pip3 and python3 to specify that you're not using version 2.
Open up your terminal, and type or paste in the following:
1. `git clone "https://github.com/DaEliteCoder/Timerist.git"`
2. `cd Timerist && cd src && pip install -r requirements.txt && cd auth && python3 -u Auth.py`
---
#### Optional: To check if the dependencies were installed properly, type or paste in the following in your terminal: 
`pip3 freeze`

Notices
===

<p>Binaries and Executables will be realeased in the near future with the deployment of this app 😀.</p>

License
===
<a href="https://github.com/TheEliteCoder1/Timerist/blob/main/src/LICENSE">BSD 2-Clause "Simplified"</a>

Code Insight
===
<h2>How Timerist works:</h2>
<h3>Timerist works alot with the user data of the logged in user. It requires a user before entering the application, and then profiles the user. On the exit of the application, Timerist saves the changes to the data done by the user. This is essentially the 'Flow of Auth' in our app.</h3>

## Auth -> Application -> Exit

<br>

Development Checklist
===
<h2>The following checklist regards the development requirements for the first release of Timerist:<h2> 

- [ ] More Features
- [ ] Bug Free
- [ ] Polishing
- [ ] Migration from local User Data to Server Side
- [x] Finish the Editor Settings
- [ ] Finish User Settings
- [ ] Create Executable & Installer
- [ ] Django Website to Download for Free

<br>

Settings-API
===
<h2>Here, I would like to introduce to you our new JSON Settings API. It is still in development, but I will update it's progress and document it here.</h2>

<h2>So far we have an JSON api for the text-editor settings. Another JSON api will be made for the user settings.</h2>


## Tutorial #1: Your First Script.
<h3>Every user has an 'editor_settings.json' file located in thier user data folder. This folder is local. We will be migrating it to server side later (to prevent the auth errors that come locally and etc.). You can find your user data in the following directory: </h3>

`/src/users/<your-email>/`

<h3>For this, I have registered an example account. So, the path to the user data of my account will look like this: </h3>

`/src/users/jeffbob@gmail.com/`

<h3>Now, to see our user data we must cd into that directory and list the directory: </h3>

1. `cd /src/users/jeffbob@gmail.com`
2. `ls` or `dir` or equivalent on your platform.

<h3>Here, we will see this: </h3>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/editor_settings.png">
