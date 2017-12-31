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
$('#last-listen-search').keyup(filterRowsEvent);

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

  // Numeric date filter for last listen
  markRowsForFilterNumeric('last-listen-cell', $('#last-listen-search').val(), date=true);

  // Hide and show rows appropriately
  $('tr[filtered-out="false"]').show();
  $('tr[filtered-out="true"]').hide();
}


/**
 * markRowsForFilter - Mark table rows for filtering based on string matching
 * some text
 *
 * Function looks for all HTML elements with the specified CSS class, and does
 * string matching on their contents. If the desired text is not found, parent
 * 'tr' elements are given the attribute 'filtered-out' with the value 'true'.
 *
 * @param {string} cellClass - CSS class to search
 * @param {string} text - text to search for in cells (not case sensitive)
 */
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


/**
 * markRowsForFilterNumeric - Mark table rows for filtering based on numeric
 * values or dates
 *
 * Function looks for all HTML elements with the specified CSS class, and
 * filters based on the input text. If the input text starts with an operator
 * (<, >, <=, >=, or =), the appropriate comparison is done for the content of
 * each element. If no operator is present, defaults to string matching (via
 * markRowsForFilter).
 *
 * If the condition is not met (or desired text is not found for string
 * matching), parent 'tr' elements are given the attribute 'filtered-out' with
 * the value 'true'.
 *
 * @param {type} cellClass - CSS class to match to elements
 * @param {type} text - text for filtering based on numerical comparison or
 *     text matching
 * @param {type} date=false - whether the contents of the elements being
 *     filtered should be interpreted as dates when text paramter contains an
 *     operator
 */
function markRowsForFilterNumeric(cellClass, text, date=false) {
  text = text.trim();

  // If there is no operator, just do text matching
  if (!(hasOperator(text))) {
    markRowsForFilter(cellClass, text);
  } else {
    // Mark cells that fail the test function
    var cells = $('.CELLCLASS'.replace('CELLCLASS', cellClass));
    for (let i = 0; i < cells.length; i++) {
      let cell = cells[i];

      if (date) {
        let d = new Date(cell.text.trim());
        var testValue = d.getTime();
      } else {
        var testValue = Number(cell.text.trim());
      }

      let testFn = getComparisonFunction(text, date=date);

      if ( !(testFn(testValue)) ) {
        let parentRow = $(cell).parents('tr');
        parentRow.attr('filtered-out', 'true')
      }
    }
  }
}


/**
 * hasOperator - Determine whether a search string starts with an operator
 *
 * @param {string} text
 * @return {boolean} true if text starts with operator, false otherwise
 */
function hasOperator(text) {
  return (text.startsWith('<') || text.startsWith('>') || text.startsWith('='));
}


/**
 * getComparisonFunction - Get a comparison test fonction based on a particular
 * text input.
 *
 * E.g.: text = "> 3" --> returns a function which takes one numeric argument,
 * returning true if the value is greater than 3 and false otherwise. Assumes
 * text input does contain an operator; if no operator is found, behavior is
 * undefined. Operators inclue: <, >, <=, >=, =.
 *
 * @param {string} text - the text to create the comparison function from
 * @returns {function} testFn
 */
function getComparisonFunction(text, date=false) {
  // Define function for casting text to number
  if (date) {
    var numCast = function(txt) {
      let d = new Date(txt);
      return d.getTime();
    }
  } else {
    var numCast = function(txt) {
      return Number(txt);
    }
  }

  // Define the test function for filtering the cell
  if (text.startsWith('<=')) {
    var compareText = text.slice(2);
    var testFn = val => val <= numCast(compareText);

  } else if (text.startsWith('>=')) {
    var compareText = text.slice(2);
    var testFn = val => val >= numCast(compareText);

  } else if (text.startsWith('<')) {
    var compareText = text.slice(1);
    var testFn = val => val < numCast(compareText);

  } else if (text.startsWith('>')) {
    var compareText = text.slice(1);
    var testFn = val => val > numCast(compareText);

  } else if (text.startsWith('=')) {
    var compareText = text.slice(1);
    var testFn = val => val == numCast(compareText);
  }

  // If text is empty after the operator, redefine testFn to always return true
  if (!(compareText)) {
    testFn = val => true;
  }

  return testFn;
}


function splitOperator(text) {

}
