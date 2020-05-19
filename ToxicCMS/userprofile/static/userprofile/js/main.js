$(function() {
    const friendRequestButton = $('#request_friend');
    friendRequestButton.on('click', () => {
        let friendId = friendRequestButton.attr("data-friend-id");
        let requestUrl =  friendRequestButton.attr("data-request-url");
        let crsfToken = $('input[name=csrfmiddlewaretoken]').val();
        request_friend(friendId, requestUrl, crsfToken);
    })

    const friendAcceptButton = $('#request_accept');
    friendAcceptButton.on('click', () => {
        let friendId = friendAcceptButton.attr("data-friend-id");
        let requestUrl =  friendAcceptButton.attr("data-request-url");
        let crsfToken = $('input[name=csrfmiddlewaretoken]').val();
        accept_friend(friendId, requestUrl, crsfToken);
    })
});