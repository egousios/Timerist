<h1 align="center">Timerist's Documentation</h1>

Table of Contents
====
<!--ts-->   
* [Installation](#installation)
* [Usage](#Usage)
    * [Managing Tasks](#Managing-Tasks)
    * [Searching For Tasks](#Searching-For-Tasks)
    * [Recycling Tasks](#Recycling-Tasks)
    * [Archiving Tasks](#Archiving-Tasks)
* [Help](#Help)
    * [Settings](#Settings)
    * [User Account](#Authentication)
<!--te-->

Installation
====

1. Open up the app by creating a shortcut to Timerist.exe in the ZIP file package.

2. Click on the Shortcut every time you want to run the app.

Usage
====

Managing Tasks
------------------------------------------------

#### In The App's Interface, you should see the following in the top-left corner:

<!--Image Path Prefix-->
<!--https://github.com/TheEliteCoder1/Timerist/blob/main/-->   

<img src="screenshots/timerist-managing-tasks.png">


#### Here's what each Option does:

1. The Add Option creates a new task by promting the following Dialogue:

<img src="screenshots/add-task.png">

The following Dialogue requests for a Date and Time for when the task is to be completed. The name of the task will be added to the todo-list.

2. The Update Option updates a task to be completed if the user
has finished a task, and vice versa to make it incomplete if they change thier mind:

<img src="screenshots/all.png">

3. The View Option allows the user to see the details of the current status for a selected task.

If the task is still incomplete, and there is still time to complete it, the View Dialogue will show the amount of time left in Days, Hours, Minutes and Seconds: 

<img src="screenshots/time-left.png">

If the task is still incomplete, and there is no time to complete it, the View Dialogue will display the following message with an alarm noise:

<img src="screenshots/overdue.png">

If the task is completed, the View Dialogue will display the following message:

<img src="screenshots/task-completed.png">

4. The Refresh Option refreshes the current state of the Todo-list:

<img src="screenshots/refresh.png">

The following example shows how when you have incomplete tasks that are overdue, they will show as 'Incomplete' without giving you more insight to how much time is left without the View Option.
But if you refresh the Todo-list, it will mark the Status as Overdue instead of Incomplete.

5. The Clear Option removes all the tasks from the Todo-list and sends them to the Recycled Tab:

<img src="screenshots/recycle-confirmation.png">

If you press 'Yes', you should see an empty Todo-list:


<img src="screenshots/cleared.png">

Searching For Tasks
------------------------------------------------

#### In the App's Interface, you should see the following
below the Todo-list Options area:

<img src="screenshots/searching-for-tasks.png">

#### Here's what each Tool does:

1. The Search Bar allows you to Search for your tasks by entering the Task's Name:

<img src="screenshots/typing-in.png">

Only tasks that match the search requirement will show.

2. The Filter By Status Tool will Only display tasks that match
the requested Status. There are 4 diffrent options - All, Incomplete, Overdue, Completed.

3. The Advacned Filter Option will prompt you with the following Dialogue:

<img src="screenshots/advanced-filter.png">

There are four options to filter tasks with the Advanced Filter Tool:

<img src="screenshots/four-advanced-options.png">

1. The Filter by Due Date Option only displays tasks that match the specified due date:

<img src="screenshots/duedatefilter.png">

2. The Filter by Due Date Range Option only displays tasks that have a due date that falls between the specified range of dates including the Start Date and End Date:

<img src="screenshots/duedaterange.png">

3. The Sort By Upcoming Option sorts the tasks with the following requirements:

<img src="screenshots/sortbyupcoming.png">