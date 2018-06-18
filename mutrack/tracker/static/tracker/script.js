/*
Javascript file for tracker application.
*/

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

/** Case-insensitive contains selector */
jQuery.expr[':'].containsNoCase = function(a, i, m) {
  return jQuery(a).text().toUpperCase()
      .indexOf(m[3].toUpperCase()) >= 0;
};

//-------------------------- Function definitions ---------------------------//

/**
 * filterRowsEvent - Wrapper for filterRows in the form of an event handler.
 * Event object not necessary for the filtering.
 */
function filterRowsEvent(event) {
  filterRows();
}

/**
 * filterRows - Filter table rows on index page based on search inputs
 */
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
  markRowsForFilterNumeric(
    'last-listen-cell', $('#last-listen-search').val(), date=true);

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
 * Multiple strings to match may be included using commas for 'and' operator or
 * pipes for 'or' behavior.
 *
 * E.g.:
 * - 'metal | rock' - matches any cell with 'metal' or 'rock' in it
 * - 'indie, post rock' - matches any cell with 'indie' and 'post rock' in it
 *
 * @param {string} cellClass - CSS class to search
 * @param {string} text - text to search for in cells (not case sensitive)
 */
function markRowsForFilter(cellClass, text) {
  text = text.trim();

  // Split selections separated by commas and call function recursively
  if (text.includes(',')) {
    let textSplits = text.split(',');
    for (let i = 0; i < textSplits.length; i++) {
      markRowsForFilter(cellClass, textSplits[i]);
    }
  } else {

    var selector = '.CLS:not('.replace('CLS', cellClass);

    // Check for | for 'or'
    if (text.includes('|')) {
      let textSplits = text.split('|');

      // Construct selector
      for (let i = 0; i < textSplits.length; i++) {
        let subText = textSplits[i].trim();
        selector = selector.concat(
          getIndividualFilterSelector(cellClass, subText));
        if (i != textSplits.length-1) {
          selector = selector.concat(', ');
        }
      }

    } else {
      // Find cells with given class that don't contain the text
      selector = selector.concat(getIndividualFilterSelector(cellClass, text));
    }

    selector = selector.concat(')')

    console.log(selector);

    // Mark the rows using the 'filtered-out' attribute
    let nomatch = $(selector);
    let rowsToMark = nomatch.parents('tr');
    rowsToMark.attr('filtered-out', 'true');
  }
}


/**
 * getIndividualFilterSelector - get selector for text filtering
 *
 * Get a CSS selector (for jQuery) for selecting all elements of a given
 * class based on some text from a search input.
 *
 * Nominally, the selector will simply do case-insensitive string matching
 * based on filterText. This behavior is changed if filterText contains any
 * of the following special characters:
 * - If the text starts with '!', will return a selector for elements that
 *   do *not* contain the given text
 *
 * filterText should not have any leading/trailing whitespace
 *
 * @param  {string} cellClass  class of elements being filtered
 * @param  {string} filterText text we are filtering on
 * @return {type}            description
 */
function getIndividualFilterSelector(cellClass, filterText) {

  // Put together base selector
  if (filterText.startsWith('!')) {
    filterText = filterText.substring(1);
    var selector =
      ".CLS:not(.CLS:containsNoCase('TEXT'))".replace('CLS', cellClass);
  } else {
    var selector = ".CLS:containsNoCase('TEXT')";
  }
  // Put in the filtering text and class
  selector = selector.replace('TEXT', filterText);
  selector = selector.replace('CLS', cellClass);

  return selector;
}

/**
 * markRowsForFilterNumeric - Mark table rows for filtering based on numeric
 * values or dates
 *
 * Function looks for all HTML elements with the specified CSS class, and
 * filters based on the input text. If the input text starts with an operator
 * (<, >, <=, >=, or =), the appropriate comparison is done for the content of
 * each element. If no operator is present, defaults to case-insensitive string
 * matching.
 *
 * Multiple conditions may be imposed using commas for 'and' operator or using
 * pipes for 'or' behavior.
 * E.g.:
 *  - '>2016 | <2011' matches strings with numbers greater than 2016 or less
 *    than 2011
 * - '>=2000, <2005' matches strings with numbers between 2000 and 2004
 *   inclusive
 *
 * If the overall search condition is not met, parent 'tr' elements are given
 * the attribute 'filtered-out' with the value 'true'.
 *
 * @param {string} cellClass - CSS class to match to elements
 * @param {string} text - text for filtering based on numerical comparison or
 *     text matching
 * @param {string} date=false - whether the contents of the elements being
 *     filtered should be interpreted as dates when text paramter contains an
 *     operator
 */
function markRowsForFilterNumeric(cellClass, text, date=false) {
  text = text.trim();

  // Split multiple selections by comma, and recursively call function for each
  if (text.includes(',')) {
    let textSplits = text.split(',');
    for (let i = 0; i < textSplits.length; i++) {
      markRowsForFilterNumeric(cellClass, textSplits[i], date=date);
    }
  } else {

    let allCells = $('.'.concat(cellClass));

    let textList = text.split('|');
    let testFunctions = [];

    // Construct the testFn as a chain of or's
    for (let i = 0; i < textList.length; i++) {
      testFunctions.push(getComparisonFunction(textList[i].trim(), date=date));
    }

    // Get the test function for determining whether a cell's contents meet
    // the filter criteria
    // let testFn = getComparisonFunction(text, date=date);
    let testAllCriteria = function(text) {
      for (let i = 0; i < testFunctions.length; i++) {
        let testFn = testFunctions[i];
        if (testFn(text)) {
          return true;
        }
      }
      return false;
    }

    // Mark cells that fail the test function
    for (let i = 0; i < allCells.length; i++) {
      let cell = allCells[i];

      if ( !(testAllCriteria(cell.text.trim())) ) {
        let parentRow = $(cell).parents('tr');
        parentRow.attr('filtered-out', 'true')
      }
    }
  }
}


/**
 * stringReplaceAll - Replace all instances of a substring in a string
 *
 * @param {string} text - text to do replacing on
 * @param {string} toReplace - substring to replace
 * @param {string} replaceWith - substring to put in place of toReplace
 * @return {string} - resulting string
 */
function stringReplaceAll(text, toReplace, replaceWith) {
  while (text.includes(toReplace)) {
    text = text.replace(toReplace, replaceWith);
  }
  return text;
}

/**
 * hasOperator - Determine whether a search string starts with an operator
 *
 * @param {string} text (should have no left padding)
 * @return {boolean} true if text starts with operator, false otherwise
 */
function hasOperator(text) {
  return (
    text.startsWith('<') || text.startsWith('>') || text.startsWith('='));
}

/**
 * getComparisonFunction - Get a comparison test function based on a particular
 * text input.
 *
 * E.g.: text = "> 3" --> returns a function which takes one string argument,
 * returning true if the value is greater than 3 and false otherwise.
 *
 * If text starts with an operator, assumes input to the resulting function is
 * to be cast to a number. Input is treated as a date and cast to number using
 * Date.getTime if date=true (otherwise uses Number). If no operator is
 * present, resulting test function just does case-insensitive string matching.
 * Resulting test function always takes a string as an input. Operators
 * include: <, >, <=, >=, =.
 *
 * Text should have no whitespace padding.
 *
 * @param {string} text - the text to create the comparison function from
 * @param {boolean} date=false - if true and operator is found, treat input to
 *   returned test function as date string
 * @returns {function} - resulting test function which takes one string as an
 *   argument and returns a boolean
 */
function getComparisonFunction(text, date=false) {

  // Define the test function for filtering the cell
  // If no operator is present in the text, just do case-insensitive string
  // matching
  let stringMatch = (!(hasOperator(text)));
  if (stringMatch && text.startsWith('!')) {
    text = text.substring(1);
    var testFn =
      cellStr => (!cellStr.toUpperCase().includes(text.toUpperCase()));
  } else if (stringMatch) {
    var testFn =
      cellStr => cellStr.toUpperCase().includes(text.toUpperCase());
  } else {
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

    if (text.startsWith('<=')) {
      var compareText = text.slice(2);
      var testFn = cellStr => numCast(cellStr) <= numCast(compareText);

    } else if (text.startsWith('>=')) {
      var compareText = text.slice(2);
      var testFn = cellStr => numCast(cellStr) >= numCast(compareText);

    } else if (text.startsWith('<')) {
      var compareText = text.slice(1);
      var testFn = cellStr => numCast(cellStr) < numCast(compareText);

    } else if (text.startsWith('>')) {
      var compareText = text.slice(1);
      var testFn = cellStr => numCast(cellStr) > numCast(compareText);

    } else if (text.startsWith('=')) {
      var compareText = text.slice(1);
      var testFn = cellStr => numCast(cellStr) === numCast(compareText);
    }

    // If text is empty after the operator, redefine testFn to always return
    // true
    if (!(compareText)) {
      testFn = val => true;
    }
  }

  return testFn;
}
