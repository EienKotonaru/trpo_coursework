$(document).ready(function(){
    type_selector = $('#request_type');
    type_selector.select();
    type_selector.change(() => {
            if (type_selector.val() === '1') {
                $('#create_doc').show();
                $('#create_tsr').hide();
            }
            else if (type_selector.val() === '2') {
                $('#create_doc').hide();
                $('#create_tsr').show();
            }
        }
    )
  });
