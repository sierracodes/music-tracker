# Music Tracker

This project is a Django-based web application for keeping track of albums I
listen to.

Whenever I listen to a album, I log it in this application, and add it to the
database if it's the first time I've listened to it. The application is being
developed to replace a bloated Excel spreadsheet I've been using for years for
this purpose.

## Features

### Single-column filtering

Text-based filtering including logical and (","), logical or ("|"), and logical not ("!") operators.

<img src="docs/img/genre-filter.gif" alt="Gif demonstrating filtering tabular album data based on genre">

### Multi-column filtering

Filter on multiple columns at once, and use numerical comparison operators for numerical and date fields.

<img src="docs/img/multi-filter.gif" alt="Gif demonstrating filtering tabular album data based on genre, plus album year and last listen date">

### Adding new artists, albums, and album listens

<img src="docs/img/new-artist-and-album.gif" alt="Gif showing flow of adding a new artist, then album, then listen to the table">

### Open in YouTube

One-click link for searching for an album on YouTube.

<img src="docs/img/open-in-youtube.gif" alt="Gif showing flow of adding a new artist, then album, then listen to the table">
