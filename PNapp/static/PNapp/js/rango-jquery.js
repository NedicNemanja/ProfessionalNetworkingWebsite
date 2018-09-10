$(document).ready(function() {
  $(".post-actions").click(function(event) {
      event.preventDefault();
      var pid=$(this).attr("data-postid");

      $.get('/interest', {post_id : pid }, function(data){
              alert(pid);
              $(this).removeClass('post-actions').addClass('comment-form')
      });
  });
});
