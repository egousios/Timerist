<div style="margin-left: 50px">
<h1>Timerist (In Construction 👷 🚧)</h1>
<img alt="Stars" src="https://img.shields.io/badge/build-passing-brightgreen">
<img alt="Echo" src="https://img.shields.io/github/issues-raw/DaEliteCoder/Timerist">
<h4>An application that will help students organize their day at school :)</h4>
</div>
<br>

### Images/Samples of our application:
---
#### light and dark theme mode:
<img src="images/main.png">
<img src="images/notes.png">
<img src="images/main-dark.png">
<img src="images/notes-dark.png">



### My Codebase Structure:
| Folder/File     | Purpose       
| -------------   |:-------------:
| Resource        | The Resource package is a utility composed of modules, classes, & functions that can help us easily break down implementations for GUI. 
| database        | A folder database that handles the notes created by the user in the application.      
| images          | A folder that contains image resources for the application and the "README.md" file.
| README.md       | A markdown file describing our application, and the underlying source code that works behind the scenes to help the user organize their day at school.
| alarm.gif       | A gif file that is shown when one of the tasks that the user has created in the "to do" section, has not been completed by the assigned date and time.
| alarm.wav       | A wav file that is played alongside the "alarm.gif" file to show the user that the time is up, and that they need to complete their task as soon as possible to stay on time.
| app.py          | A module that combines all other source files, and runs the application.
| blueprint       | A blueprint for the requirements that our application needs to meet at the minimum.
| data.txt        | A textfile that acts as a "database" for all the todos that the user has made in the application's "todo" section.
| interface.ui    | A .ui file composed of qml tags that were at first, the user interface our application which had been expanded and improved by python code.
| light-theme.qss | A .qss file that is a stylesheet for our application.
| requirements.txt | A text file containing the required dependencies that are needed in order to run this application from source.

### Running from source (Windows):
Make sure that you have 'pip' installed on your system, and that you have added it to your Python path.
If you have completed the step above, you may move on to completing the steps below.
Open up your terminal, and type or paste in the following:
1. `git clone "https://github.com/DaEliteCoder/Timerist.git"`
2. `cd Timerist`
3. `pip install requirements.txt`
4. `python -u app.py`
### Running from source (MacOS / Linux):
Make sure that you have 'pip' installed on your system, and that you have added it to your Python path.
If you have completed the step above, you may move on to completing the steps below. Remember, Python version 2 is pre-installed on your operating system, so you will have to say pip3 and python3 to specify that you're not using version 2.
Open up your terminal, and type or paste in the following:
1. `git clone "https://github.com/DaEliteCoder/Timerist.git"`
2. `cd Timerist`
3. `pip3 install requirements.txt`
4. `python3 -u app.py`

### Note: Binaries and Executables will be realeased in the near future, as a part of the distribution of this application 😀.






