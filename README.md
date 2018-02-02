# Music Tracker

This project is a Django-based web application for keeping track of albums I
listen to.

Whenever I listen to a album, I log it in this application, and add it to the
database if it's the first time I've listened to it. The application is being
developed to replace a bloated Excel spreadsheet I've been using for years for
this purpose.

#### Current Features
* Tabular display of all albums on index page, including search/filter
  functionality including comparison operators for numeric/date fields (i.e.
    =, <, >, <=, >=), and logical or operation with pipe |
* Detail pages for each album, including link to search
  for the album on YouTube
* Detail pages for artists, including a list of all the
  albums in the database by that artist
* Listen tracking for each album
* Add/edit functionality for artist/album

#### To do
* Add ability to delete albums/artists
* Improve responsiveness for future mobile support, e.g. add breakpoints to
  hide some table columns for less wide screens
