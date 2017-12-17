# Music Tracker

This project is a Django-based web application for keeping track of albums I
listen to.

Whenever I listen to a album, I log it in this application, and add it to the
database if it's the first time I've listened to it. The application is being
developed to replace a bloated Excel spreadsheet I've been using for years for
this purpose.

#### Current Features
* Tabular display of all albums on index page, including rudimentary
  search/filter functionality.
* Detail pages (still somewhat sparse) for each album, including link to search
  for the album on YouTube
* Detail pages (also sparse) for artists; currently just a list of all the
  albums in the database by that artist

#### To do
* Implement listen logging (including loading in listen data from my Excel
  spreadsheet)
* Add ability to add/edit albums
* Improve search behavior for year, rating, genre (better than just string
  matching)
