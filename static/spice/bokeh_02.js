
function openMode(evt, tabMode) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabMode).style.display = "block";
  evt.currentTarget.className += " active";

};

function Simulation(sim_type){

  var properties = [];
  var sel = $("#"+sim_type+" input");

  sel.each(function(){
    var new_element = {};
    var n = $(this)[0].name;
    var v = $(this)[0].value;
    new_element[n] = v ;
    properties.push(new_element);
  });


  var data = new Object();
  data["type"] = sim_type;
  data["properties"] = properties;
  // data['spice'] = spice;
  // alert(spice);

  // for(var i=0; i<properties.length; i++){
  //   var key = Object.keys(properties[i])[0];
  //   var val = Object.values(properties[i])[0];
  //   alert(key + " "+ val);
  // }

  // $.ajax({
  //     type: 'POST',
  //     url: "/simulation",
  //     data: data,
  //     success: function (response) {
  //         alert(response);
  //     }
  // });

}
