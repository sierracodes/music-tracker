/*
Javascript file for tracker application.
*/

// Case-insensitive contains selector
jQuery.expr[':'].containsNoCase = function(a, i, m) {
  return jQuery(a).text().toUpperCase()
      .indexOf(m[3].toUpperCase()) >= 0;
};

// Attach event handlers for search inputs
$('#artist-search').keyup(filterRows);
$('#album-search').keyup(filterRows);
$('#year-search').keyup(filterRows);
$('#rating-search').keyup(filterRows);
$('#genre-search').keyup(filterRows);
$('#plays-search').keyup(filterRows);

// Filter rows based on search inputs
function filterRows(event) {

  // Start by marking all rows as not filtered out
  var allRows = $('.album-data-row');
  for (i = 0; i < allRows.length; i++) {
    let row = allRows[i];
    row.setAttribute('filtered-out', 'false');
  }

  // Mark rows as filtered out according to the search inputs
  markRowsForFilter('artist-cell', $('#artist-search').val());
  markRowsForFilter('album-cell', $('#album-search').val());
  markRowsForFilter('year-cell', $('#year-search').val());
  markRowsForFilter('rating-cell', $('#rating-search').val());
  markRowsForFilter('genre-cell', $('#genre-search').val());
  markRowsForFilter('plays-cell', $('#plays-search').val());

  // Hide and show rows appropriately
  $('tr[filtered-out="false"]').show();
  $('tr[filtered-out="true"]').hide();
}

// Mark all table cells of a given class which do not contain a given text
// string (not case sensitive)
function markRowsForFilter(cellClass, text) {

  // Find cells with given class that don't contain the text
  let selector = ".CELLCLASS:not(.CELLCLASS:containsNoCase('TEXT'))"
  selector = selector.replace('CELLCLASS', cellClass);
  selector = selector.replace('CELLCLASS', cellClass);
  selector = selector.replace('TEXT', text);
  var nomatch = $(selector);

  // Mark the rows using the 'filtered-out' attribute
  var rowsToMark = nomatch.parents('tr');
  for (i = 0; i< rowsToMark.length; i++) {
    let row = rowsToMark[i];
    row.setAttribute('filtered-out', 'true');
  }
}
