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

<br>

Settings-API
===
<h4>Here, I would like to introduce to you our new JSON Settings API. It is still in development, but I will update it's progress and document it here.</h4>

<h4>So far we have an JSON api for the text-editor settings. Another JSON api will be made for the user settings.</h4>


## Tutorial #1: Your First Script.
<p>Every user has an 'editor_settings.json' file located in thier user data folder. This folder is local. We will be migrating it to server side later (to prevent the auth errors that come locally and etc.). You can find your user data in the following directory: </p>

`/src/users/<your-email>/`

<p>For this, I have registered an example account. So, the path to the user data of my account will look like this: </p>

`/src/users/jeffbob@gmail.com/`

<p>Now, to see our user data we must cd into that directory and list the directory: </p>

1. `cd /src/users/jeffbob@gmail.com`
2. `ls` or `dir` or equivalent on your platform.

<p>Here, we will see this: </p>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/editor_settings.png">

<p>Now, we can open up our 'editor_settings.json' file and edit it. Here, we will write the following: </p>

<p>Make sure to add your json body (pair of curly braces): </p>

<p>body: 

`{}`

<p>Inside of our body, we can place either one of these properties: </p>

1. `"'background-color'": "'(255, 0, 13, 255)"'` value: `rgb or rgba`
2. `"'background-image'": "'path-to-image"'` value: `path`

<p>If you put both properties for the background, it will not work.</p>

<p>Note: We don't have support for diffrent types of strings yet, so please just use the following string format when writing/editing these properties.This file contains the settings properties for the text editor in Timerist, so the background color/image will apply to the editor!. So, the editor's settings can be changed through this json script, or directyly within the settings menu of the editor. The settings menu of the editor saves and loads the data to this script.</p>

<p>After setting the background appearance of our editor, we can change 1 property that has
to do with our preferances.</p>

<p>If you haven't noticed yet, everytime we finish editing a document in the editor andwe decide to close it, there's a pop-up save dialog. This is to make sure that we don't forget to save our changes by hitting the save button or `ctrl-s`. We can choose wether we want this dialog to show or not simply by toggling it in the preferances tab. (Editor Settings->Preferances->Show Save Dialog On Close):</p>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/toggle_settings.png">

<p>In our JSON API, the equivalent is: </p>

`"'save-on-close'": "'False'"` value: `boolean enclosed in string`

<p>Now, our settings script should look like this: </p>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/editor_json.png">

<p>Moving on with this tutorial, you can open & edit the json file directly in the settings menu instead of elsewhere using this 'settings to json' option that I just implemented recently.</p>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/json.png">

## All Settings Properties: editor_settings.json

| Property                                                      | Code                                      | Purpose
| ---                                                           | ---                                       | ---
| <p style="text-shadow: 2px 2px #55d5e0">background-color</p>  | `"'background-color'": "'(r, g, b, a)"'`  | <p>Sets the background appearance of the editor with a color.</p> 
| <p style="text-shadow: 2px 2px #55d5e0">background-image</p>  | `"'background-image'": "'absolute path"'` | <p>Sets the background appearance of the editor with an image.</p>
| <p style="text-shadow: 2px 2px #55d5e0">save-on-close</p>     | `"'save-on-close'": "'True or False"'`    | <p>Control wether the save dialog should show when you close the editor.</p>

## Fetching The Settings From the API
<h4>I've created a web api for the settings, this way you can 
access your json settings through a URL. The API is still in development, and is quite fast because it uses FastAPI for the backend:<h4>

<a href="https://github.com/tiangolo/fastapi#readme">FastAPI</a>

#### Running the Server
<p>To run the server, you will need to do the following:</p>

1. Install Uvicorn: `pip install uvicorn`.
2. Go to the `json_settings_api` folder.
3. And then run the following: `uvicorn main:app --reload`
4. Now, you can access the API by going to: <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a>

<p>If everything went well, then you will see this: </p>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/message.png">


#### Usage
<p>Here's some sample usage of the API to fetch your editor_settings data: </p>

The Root: `/`
The Users Route: `/users`
Accessing Your Account: `/users/<user_email>`
Accessing Your Data: `/users/<user_email>/<settings_filename>`
Sample: `/users/jeffbob@gmail.com/editor_settings.json`

<p>If you're request URL was valid, you should see something like this: </p>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/message2.png">

<p>If you're request URL was not valid, you will recieve a 404 HTTP Response: </p>

<img src="https://github.com/TheEliteCoder1/Timerist/blob/main/src/images/message3.png">

Development Checklist
===
<h4>The following checklist regards the development requirements for the first release of Timerist:<h4> 

- [ ] More Features
- [ ] Bug Free
- [ ] Polishing
- [ ] Migration from local User Data to Server Side
- [x] Finish the Editor Settings
- [ ] Finish User Settings
- [ ] Create Executable & Installer
- [ ] Django Website to Download for Free

Notices
===

<p>Binaries and Executables will be realeased in the near future with the deployment of this app 😀.</p>

License
===
<a href="https://github.com/TheEliteCoder1/Timerist/blob/main/src/LICENSE">BSD 2-Clause "Simplified"</a>