$(document).ready(function(){
    type_selector = $('#request_type');
    type_selector.select();
    type_selector.change(
        () => console.log(type_selector.val())
    )
  });
