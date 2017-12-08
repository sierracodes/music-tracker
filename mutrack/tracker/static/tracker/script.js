

// Case-insensitive contains selector
jQuery.expr[':'].containsNoCase = function(a, i, m) {
  return jQuery(a).text().toUpperCase()
      .indexOf(m[3].toUpperCase()) >= 0;
};


// Attach event handlers for search inputs
$("#album-search").keyup(filterAlbums);

function filterAlbums(event) {
  var text = event.target.value;

  var selectingOn = $("#search-selector").val();

  if (selectingOn === "artist") {
    var match = $(".artist-cell:containsNoCase('text')".replace('text', text));
    var nomatch = $(".artist-cell:not(.artist-cell:containsNoCase('text'))".replace('text', text));
  }
  else if (selectingOn === "album") {
    var match = $(".album-cell:containsNoCase('text')".replace('text', text));
    var nomatch = $(".album-cell:not(.album-cell:containsNoCase('text'))".replace('text', text));
  }
  else if (selectingOn === "year") {
    var match = $(".year-cell:containsNoCase('text')".replace('text', text));
    var nomatch = $(".year-cell:not(.year-cell:containsNoCase('text'))".replace('text', text));
  }
  else if (selectingOn === "genres") {
    var match = $(".genre-cell:containsNoCase('text')".replace('text', text));
    var nomatch = $(".genre-cell:not(.genre-cell:containsNoCase('text'))".replace('text', text));
  }
  match.parents('tr').show();
  nomatch.parents('tr').hide();


}
