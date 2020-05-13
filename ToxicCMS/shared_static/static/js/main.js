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
            dataType: "json",
            data: {
                search_value: search_value,
            },
            success: function (response) {
                console.log(response);
                showFoundProfiles(response);
            },
        })
    }

    function showFoundProfiles(value) {
        profile_list.html('');
        value.forEach(p => {
            let innerHtml = `
                <li>
                <a href="/${p.username}"><div>${p.username}</div></a>`;
            if (p.isFriend) {
                innerHtml += `<a href="wrap with form and make post"><div>+</div></a>`;
                innerHtml += `</li>`;
            }

            profile_list.html(innerHtml);
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

