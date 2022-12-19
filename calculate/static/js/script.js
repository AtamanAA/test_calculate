$(document).ready(function(){
  
   
});


// Script for highlighting the selected menu section
if (document.title == "Різьба") {            
  $("#thread").addClass('active')                     
}
else if (document.title == "Труба") {
  $("#pipe").addClass('active')                
}
else if (document.title == "Матеріали") {
  $("#materials").addClass('active')                
}
else {
  $("#home").addClass('active')        
}
