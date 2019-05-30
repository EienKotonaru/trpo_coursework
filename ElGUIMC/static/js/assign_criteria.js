$(document).ready(function(){
    $('.assigned').change((e) => {
            if ($(e.target).is(':checked')) {
                let parent_row = e.target.parentNode.parentNode.parentNode.parentNode;
                $(parent_row).find('.weight_div').show();
            } else {
                let parent_row = e.target.parentNode.parentNode.parentNode.parentNode;
                $(parent_row).find('.weight_div').hide();
                $(parent_row).find('.weight_input').val('');
            }
        })
  });
