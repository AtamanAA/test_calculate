$(document).ready(function(){
  
   
});


// Скрипт подсвечивания выбраного раздела меню, возможно поменять на функцию
if (document.title == "Різьба") {            
  $("#thread").addClass('active')                     
}
else if (document.title == "Труба") {
  $("#pipe").addClass('active')                
}
else {
  $("#home").addClass('active')        
}
