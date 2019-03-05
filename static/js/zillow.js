$('.getZillow').on('click', function() {
  var currentRow = $(this).parent(); //tr
  var ssl = currentRow.children("#ssl_value").text();
  var proptype = currentRow.children("#proptype_value").text();
  var address = currentRow.children("#premiseadd_value").text();
  var address2 = currentRow.children("#address2_value").text();
  var owner = currentRow.children("#owner_value").text();
  var owner2 = currentRow.children("#owner2_value").text();
  var status_tbl_element = currentRow.children("#status_value");
  var city_state = 'WASHINGTON DC'

  //console.log(currentRow.html())

  var request = new XMLHttpRequest();
  request.open('GET', '/zillow_status?&address='+address+'&citystatezip='+city_state, true);

  request.onload = function() {

    // Begin accessing JSON data here
    var data = JSON.parse(this.responseText);
    var link = data[0]
    var status = data[1]
    var tbl = $("<td></td>");
    //console.log(link +' '+status);
    tbl.attr("style","text-align:center");
    var txt = $("<a></a>").text(status);
    txt.attr("href",link);
    txt.attr("target","_blank");
    txt.attr("style","text-align:center");
    tbl.append(txt);
    status_tbl_element.replaceWith(tbl);
    //console.log(status_tbl_element.children().text())
  }

  request.send();


});
