window.addEventListener("load", function() {

  // Add a keyup event listener to our input element
  var owner_input = document.getElementById('owner_input');
  owner_input.addEventListener("keyup", function(event) {
    owner_hinter(event)
  });

  // create one global XHR object
  // so we can abort old requests when a new one is made
  window.hinterXHR = new XMLHttpRequest();
});

// Autocomplete for form
function owner_hinter(event) {

  // retireve the input element
  var input = event.target;


  // minimum number of characters before we start to generate suggestions
  var min_characters = 0;

  if (input.value.length < min_characters) {
    return;
  } else {

    // abort any pending requests
    window.hinterXHR.abort();

    window.hinterXHR.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {

        // We're expecting a json response so we convert it to an object
        var response = JSON.parse(this.responseText);

        $('#owner_input').autocomplete({
          source: response,
        });
      }
    };
    //normalise to uppercase when sending
    window.hinterXHR.open("GET", "/owner_autocomplete?search_term="+input.value.toUpperCase(), true);
    //send request
    window.hinterXHR.send()
  }
}
