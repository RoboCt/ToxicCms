$(document).on('submit', '#new_feed_form', (event) => {
    event.preventDefault();

    $.ajax({
            url: $('#new_feed_form').attr("data-newFeed-url"),
            type: "POST",
            dataType: "html",
            data: {
                title: $('#id_title').val(),
                content: $('#id_content').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                $('#id_title').val("");
                $('#id_content').val("");
                $('#feed_list').prepend(response)
            },
        })

});
