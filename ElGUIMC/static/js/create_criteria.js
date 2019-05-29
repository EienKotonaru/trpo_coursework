$(document).ready(function(){
    $('#add_criteria').click((event) => {
        event.preventDefault();
        add_new_criteria($('#criteria_template'));
    });

    const last_criteria = $('.criteria:last');
    const counter = parseInt(last_criteria.attr('id'));

    for(let i = 0; i <= counter; i++) {
        const delete_button = $('#' + i).find('.delete_criteria');
        add_button_remover(delete_button);

        const save_button = $('#' + i).find('.save_criteria');
        add_button_saver(save_button);
    }
});

function add_new_criteria(criteria_template) {
    const last_criteria = $('.criteria:last');
    const counter = parseInt(last_criteria.attr('id'));
    criteria_template.clone().insertAfter(last_criteria).attr('id', counter + 1).show();
    $('#' + (counter + 1)).find('.select-wrapper').remove();
    $('select').select();

    const delete_button = $('#' + (counter + 1)).find('.delete_criteria');
    add_button_remover(delete_button);

    const save_button = $('#' + (counter + 1)).find('.save_criteria');
    add_button_saver(save_button);
}

function add_button_saver(button_selector) {
    button_selector.on("click", (event) => {
        event.preventDefault();
        const url = $(location).attr('href');
        const parts = url.split("/");
        const group_id = parts[parts.length-1];

        const current_row = button_selector.parent().parent();
        $.ajax({
            method: "POST",
            url: "/add_criteria/" + group_id,
            data: {
                type: "save",
                name: current_row.find("input[name=name]").val(),
                measure: current_row.find("input[name=measure]").val(),
                csrfmiddlewaretoken: current_row.parent().find("input[name=csrfmiddlewaretoken]").val()
            },
            success: (response) => {
                $('.criteria:last').find('.p_id').text(response["id"]);
            }
		});
    });
}

function add_button_remover(button_selector) {
    const current_form_id = button_selector.closest('form').attr('id');
    button_selector.on("click", (event) => {
        event.preventDefault();

        const url = $(location).attr('href');
        const parts = url.split("/");
        const group_id = parts[parts.length-1];
        const current_row = button_selector.parent().parent();
        $.ajax({
            method: "POST",
            url: "/add_criteria/" + group_id,
            data: {
                type: "delete",
                id: parseInt(current_row.find(".p_id").text()),
                csrfmiddlewaretoken: current_row.parent().find("input[name=csrfmiddlewaretoken]").val()
            },
            success: console.log('ok')
        });

        remove_criteria_form(current_form_id);
    });
}

function remove_criteria_form(form_id) {
    const last_id = parseInt($('.criteria:last').attr('id'));
    if(last_id !== 0) {
        $('#' + form_id).remove();
        for (let i = parseInt(form_id) + 1; i <= last_id; i++) {

            const form_selector = $('#' + i);
            const button_selector = form_selector.find('.delete_criteria');

            button_selector.off("click");
            button_selector.on("click", (event) => {
                event.preventDefault();

                const url = $(location).attr('href');
                const parts = url.split("/");
                const group_id = parts[parts.length-1];
                const current_row = button_selector.parent().parent();
                $.ajax({
                    method: "POST",
                    url: "/add_criteria/" + group_id + "/",
                    data: {
                        type: "delete",
                        id: parseInt(current_row.find(".p_id").text()),
                        csrfmiddlewaretoken: current_row.parent().find("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: console.log('ok')
                });

                remove_criteria_form(i - 1);
            });
            form_selector.attr('id', i - 1);
        }
    }
}