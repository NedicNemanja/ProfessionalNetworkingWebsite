/**********************index.html related*************************************/
//interest jquery for index.html
$(document).ready(function() {
  $(".post-actions").click(function(event) {
      event.preventDefault();
      var element=$(this);
      var pid=$(element).attr("data-postid");

      $.ajax({
        url: '/interest/',
        type: 'POST',
        data: { postid: pid,
                csrfmiddlewaretoken: '{{ csrf_token }}' },

        success: function(json){
          if (json.total_interests == 1)
            $(element).replaceWith("You are interested in this.");
          else
            var num = json.total_interests-1;
            $(element).replaceWith("You and "+num+" other are interested.");
        },

        error: function(json){
          alert(json.error);
        }
      });

  });
});


/**********************notifications.html related******************************/
//accept/reject request for notification.html
$(document).ready(function() {
  $('.friend_request').click(function(event) {
    event.preventDefault();
    var element = $(this);


    $.ajax({
      url: '/friend_request/',
      type: 'POST',
      data: { action: $(element).attr('name'),
              fr_id: $(element).val(),},

      success: function(json){
        $(element).closest(".col-sm-3").closest(".row").closest(".message-pointer").closest(".message-bubble").closest(".my-notification").closest(".row").remove();
      },

      error: function(){
        alert("error");
      }
    });

  });
});
