/*
Javascript file for tracker application.
*/

// Case-insensitive contains selector
jQuery.expr[':'].containsNoCase = function(a, i, m) {
  return jQuery(a).text().toUpperCase()
      .indexOf(m[3].toUpperCase()) >= 0;
};

// Attach event handlers for search inputs
$('#artist-search').keyup(filterRowsEvent);
$('#album-search').keyup(filterRowsEvent);
$('#year-search').keyup(filterRowsEvent);
$('#rating-search').keyup(filterRowsEvent);
$('#genre-search').keyup(filterRowsEvent);
$('#plays-search').keyup(filterRowsEvent);

// Run once when document is ready in case of back button
$(document).ready(filterRows);

// Row filter in form of event handler; event object not necessary for the
// filtering
function filterRowsEvent(event) {
  filterRows();
}

// Filter rows based on search inputs
function filterRows() {
  // Start by marking all rows as not filtered out
  var allRows = $('.album-data-row');
  for (i = 0; i < allRows.length; i++) {
    let row = allRows[i];
    row.setAttribute('filtered-out', 'false');
  }

  //---- Mark rows as filtered out according to the search inputs
  // Regular 'contains' filters for text cells
  markRowsForFilter('artist-cell', $('#artist-search').val());
  markRowsForFilter('album-cell', $('#album-search').val());
  markRowsForFilter('genre-cell', $('#genre-search').val());

  // Numeric fileters for year, rating, and plays
  markRowsForFilterNumeric('year-cell', $('#year-search').val());
  markRowsForFilterNumeric('rating-cell', $('#rating-search').val());
  markRowsForFilterNumeric('plays-cell', $('#plays-search').val());

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
  rowsToMark.attr('filtered-out', 'true');
}

// Specialized function for filtering based on numeric values, which can use
// comparison operators (<, >, <=, >=, and =)
function markRowsForFilterNumeric(cellClass, text) {
  text = text.trim();

  // Define the test function for filtering the cell
  if (text.startsWith('<=')) {
    var compareText = text.slice(2);
    if (compareText) {
      var testFn = val => val <= Number(compareText);
    } else {
      var testFn = val => true;
    }

  } else if (text.startsWith('>=')) {
    var compareText = text.slice(2);
    if (compareText) {
      var testFn = val => val >= Number(compareText);
    } else {
      var testFn = val => true;
    }

  } else if (text.startsWith('<')) {
    var compareText = text.slice(1);
    if (compareText) {
      var testFn = val => val < Number(compareText);
    } else {
      var testFn = val => true;
    }

  } else if (text.startsWith('>')) {
    var compareText = text.slice(1);
    if (compareText) {
      var testFn = val => val > Number(compareText);
    } else {
      var testFn = val => true;
    }

  } else if (text.startsWith('=')) {
    var compareText = text.slice(1);
    if (compareText) {
      var testFn = val => val == Number(compareText);
    } else {
      var testFn = val => true;
    }

  } else {
    var compareVal = -1;
    var testFn = val => val.toUpperCase().includes(text.toUpperCase());
  }

  // Mark cells that fail the test function
  var cells = $('.CELLCLASS'.replace('CELLCLASS', cellClass));
  for (let i = 0; i < cells.length; i++) {
    let cell = cells[i];
    if ( !(testFn(cell.text.trim())) ) {
      let parentRow = $(cell).parents('tr');
      parentRow.attr('filtered-out', 'true')
    }
  }
}
