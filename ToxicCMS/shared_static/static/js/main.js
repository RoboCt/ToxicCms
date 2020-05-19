$(function() {
    const search_box = $('#friend_search');
    const profile_list = $('#profiles_list');
    const delay_ms = 800;
    let search_function = false;

    search_box.val('');

    function find_friends(search_value) {
        $.ajax({
            url: search_box.attr("data-find-url"),
            type: "GET",
            dataType: "html",
            data: {
                search_value: search_value,
            },
            success: function (response) {
                console.log(response);
                profile_list.html(response);
            },
        })
    }

    search_box.on('keyup', () => {
        let value = $('#friend_search').val();
        if (search_function) {
            clearTimeout(search_function)
        }
        if (value === '') {
            profile_list.html('');
        } else if (value.length > 2) {
            console.log(value.length);
            search_function = setTimeout(find_friends, delay_ms, value);
        }
    });
});

