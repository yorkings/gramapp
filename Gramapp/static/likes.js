$(document).ready(function() {
    $('.like-link').on('click', function(event) {
        event.preventDefault();
        var postId = $(this).data('post-id');
        var likeCountElement = $(this).closest('.post-footer').find('.post-likes h5');
        
        // Send an AJAX request to record the like
        $.ajax({
            url: '{% url "like" 0 %}'.replace('0', postId),
            type: 'POST',
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(response) {
                if (response.success) {
                    // Update the like count on the page
                    var likes = response.likes;
                    likeCountElement.text(likes + ' likes');
                }
            }
        });
    });
});
