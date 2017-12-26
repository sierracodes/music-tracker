/*
Javascript file for tracker application.
*/

// Case-insensitive contains selector
jQuery.expr[':'].containsNoCase = function(a, i, m) {
  return jQuery(a).text().toUpperCase()
      .indexOf(m[3].toUpperCase()) >= 0;
};

// Attach event handlers for search inputs
$("#artist-search").keyup(filterArtist);
$("#album-search").keyup(filterAlbum);
$("#year-search").keyup(filterYear);
$("#rating-search").keyup(filterRating);
$("#genre-search").keyup(filterGenre);
$("#play-search").keyup(filterPlays);

function filterArtist(event) {
  var text = event.target.value;
  var match = $(".artist-cell:containsNoCase('text')".replace('text', text));
  var nomatch = $(".artist-cell:not(.artist-cell:containsNoCase('text'))".replace('text', text));
  match.parents('tr').show();
  nomatch.parents('tr').hide();
}
function filterAlbum(event) {
  var text = event.target.value;
  var match = $(".album-cell:containsNoCase('text')".replace('text', text));
  var nomatch = $(".album-cell:not(.album-cell:containsNoCase('text'))".replace('text', text));
  match.parents('tr').show();
  nomatch.parents('tr').hide();
}
function filterYear(event) {
  var text = event.target.value;
  var match = $(".year-cell:containsNoCase('text')".replace('text', text));
  var nomatch = $(".year-cell:not(.year-cell:containsNoCase('text'))".replace('text', text));
  match.parents('tr').show();
  nomatch.parents('tr').hide();
}
function filterRating(event) {
  var text = event.target.value;
  var match = $(".rating-cell:containsNoCase('text')".replace('text', text));
  var nomatch = $(".rating-cell:not(.genre-cell:containsNoCase('text'))".replace('text', text));
  match.parents('tr').show();
  nomatch.parents('tr').hide();
}
function filterGenre(event) {
  var text = event.target.value;
  var match = $(".genre-cell:containsNoCase('text')".replace('text', text));
  var nomatch = $(".genre-cell:not(.genre-cell:containsNoCase('text'))".replace('text', text));
  match.parents('tr').show();
  nomatch.parents('tr').hide();
}
function filterPlays(event) {
  var text = event.target.value;
  var match = $(".plays-cell:containsNoCase('text')".replace('text', text));
  var nomatch = $(".plays-cell:not(.plays-cell:containsNoCase('text'))".replace('text', text));
  match.parents('tr').show();
  nomatch.parents('tr').hide();
}
