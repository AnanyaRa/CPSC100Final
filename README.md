# Documentation

"The Yale Weekly", created by Ananya Rajagopalan ('24) and Marcella Villagomez ('24)

## YouTube Link to Demo Video

https://youtu.be/RQQRhoF7s0M

## Compiling/Starting "The Yale Weekly" in the CS50 IDE

Commands: (Execute cd to ensure that you're in ~/ (i.e. your home directory, aka ~))

Execute cd project to change into our project's directory.
Execute export API_KEY=f3056bb039017ca9b4843ab2537f5e60 (this will ensure that the weather API works)
Execute flask run

Click on the link that is returned (comes after "Running on") to open the program.

## Registering as a new user

Click on the "Register" tab located in the right side of the bar (you're probably currently on the Log In page). You should see a form that
asks you to fill out your username, password, your password again for confirmation, and the name of the
city that you're currently located in (if not located in a city, enter the closest one). NOTE: Specifically for the "city" box, you don't have to worry about
entering a city that is properly capitalized (i.e. entering "seattle" works just as well as entering "Seattle").
If you enter information erroneously (a username that has already been taken, passwords that don't match, an invalid city name, etc.), you will be prompted with an error and should click on the "Register" tab again
to properly enter the information.

After you've successfully registered, you should be automatically redirected to the home page (no need to login here) where you will be "welcomed"!

## Logging in

If you are launching the application as a returning user, then you should see the login page as soon as you click
the link that flask run returns. To log in, enter the username and password (case sensitive) that you registered with.

If you enter this information erroneously (username that doesn't exist, incorrect password, don't enter anything, etc.) you will be prompted with an
error and should click the "Log In" tab located in the right side of the window bar to properly enter the information.

NOTE: If you forgot your username/password, you can simply create a new account by using the "Register" tab as referenced above.

After you've successfully logged in, you should be redirected to the home page where you will be "welcomed".

## Home Page

On the home page, you will see a Welcome banner that is specific to your username.
Below that, you will see the current weather for whichever city you said you were located in when you registered.
You will also see the current date, along with any events you might have scheduled for today.
If you don't have any events scheduled for today, you will see no events listed after the colon.

NOTE: To navigate to this home page from another page on the website, simply click on "The Yale Weekly" button in the
left most corner of the navigation bar.

## Adding a new event

To add a new event, click on the "Add New Event" tab in the left side of the bar.
You should be prompted with a form that asks you a series of questions, including the name of the event,
its date, a description, its start time, end time, and relative importance.

NOTE: Entering a name and date for an event are the only required fields. If you don't enter either of those, you will receive an error message, and you should click on "Add
New Event" to properly enter the information again. If you enter anything other than a capital Y or N in the importance box, you will also receive an error message and should re-try.
Also, if you enter a duplicate event, the duplicate event will be entered just like a normal event.

If you are adding an event that is for the current day (i.e. you're testing the website on a Tuesday evening and you add an event for that Tuesday evening) in the evening,
the event might not show up in your daily task list on the Home page (but it will show up normally in other places like the Calendar tab and the View All Events page). This is because the CS50 Server/datetime lookup function is operating on a
different time zone (that is ahead). As a result, if you add an event (in the evening where you are) that occurs the next day, it will show up on the daily task list instead.

## Looking at all the events you have

To look at all the events you've entered, click on the "View All Events" tab in the right side of the bar.

This shows you all of the events you've ever entered (not just for a certain week) ordered chronologically, specifically the name, date, description, start/end time, importance, and time entered of these events.
If you marked an event as "Y" for important, the event will show up in red. If you marked an event as "N" for not important, the event will show up in black.

## Looking at your calendar for the current week

To view your schedule for the current week, click on the "Calendar" tab in the left side of the navigation bar.
You will see just your events (and the corresponding information for each event) for the week that you currently are visiting the website during, ordered chronologically.
If you marked an event as "Y" for important, the event will show up in red. If you marked an event as "N" for not important, the event will show up in black.

NOTE: If you are viewing the calendar at the "end" of a certain week (on a Saturday), this
weekly calendar will display to you your schedule for the coming week (the week that starts on the next day, which is Sunday)
and not the week that is nearly finished.

## Deleting an Event

To delete an event that you've entered, click on the "Delete Event" tab on the right side of the navigation bar.
You will then see a input box above the list of events. Enter the name (case-sensitive, including any whitespace) of any single event you wish to delete, and then press the "Delete Event" button.
After pressing this button, that event will be deleted (both from your "All Events" record as well as potentially in your calendar if it occurred in that week).

NOTE: If you enter an invalid event (one that doesn't exist), no change will be made to your events table and/or calendar.
Additionally, if you don't enter an actual event to delete and submit a blank response, you will receive an error message and should click on the "Delete Event" tab again to correctly enter information. If you try to delete an event that repeats more than once (has the same exact name), all instances of that event will be deleted.

## Looking at the current month, past month(s) or future month(s)

To view a (blank, just the dates) calendar for any month, click on the "Monthly Calendar" tab in the left side of the navigation bar.
You can use the left/right arrows to navigate to previous/future months, and click on the "reset" button to return back to the current month.

NOTE: You aren't able to see your own events in this tab, but can always see them in the "View All Events" or "Calendar" tabs.
If you click on a date other than the current date in the current month (i.e. if today is December 6th 2020 and I click on December 8th, which is in the same month) and then click reset, your cursor will likely stay on the date that you clicked on, since you're already on the current month. If you want the day itself to reset, just click on the current day (if today is December 6th, click on December 6th). If you clicked on a date in a different month, the reset button will bring you back to the current date normally so this note doesn't apply.

## Logging Out

If you are logged in and at any time wish to log out, click the "Log Out" tab in the right side of the bar.
You will then be redirected to the Log In page.
