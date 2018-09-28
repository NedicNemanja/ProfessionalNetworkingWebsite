/**********************index.html related*************************************/
//interest jquery for index.html
$(document).ready(function() {
  $(".post_interested").click(function(event) {
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

/************************messages.html related*********************************/
//send new message
$(document).ready(function() {
  $('[name=new-mess]').click(function(event) {
    event.preventDefault();
    var element = $(this);
    var message = $(element).siblings(".form-group").children(".form-control").val();
    if( message == ""){
      alert("Write a message before sending.");
      return;
    }
    var convo_id = $(element).attr("data-convoid");

    $.ajax({
      url: '/new_message/',
      type: 'POST',
      data: { message: message,
              convo_id: convo_id,
              },

      success: function(json){
        $(element).closest(".form-inline").closest(".message-form").siblings(".panel-body").append(
          '<div class="row">'+
            '<div class="col-sm-10">'+
              '<div class="message-bubble-right">'+
                '<div class="message-pointer">'+
                  '<p>'+message+'</p>'+
                '</div>'+
                '<div class="pointer-border"></div>'+
              '</div>'+
              '<div class="clearfix"></div>'+
            '</div>'+

            '<div class="col-sm-2">'+
              '<a class="post-avatar thumbnail" href="/overview/'+json.user_id+'">'+
                '<img src="'+json.profile_photo_url+'" class="my-img-thumbnail">'+
              '</a>'+
            '</div>'+
          '<div class="clearfix"></div>'+
        '</div>');
        $(element).siblings(".form-group").children(".form-control").val('');
      },

      error: function(){
        alert("error");
      }
    });

  });
});

/*******************advertisments.html related*********************************/
//button for submitting a new ad
$(document).ready(function() {
  $('.ad_submit').click(function(event) {
    event.preventDefault();
    var skills = $(":input[name^='skill']");
    var skills_val = [];
    for(i=0; i< skills.length; i++){
      skills_val[i] = skills[i].value;
    }
    var title = $(this).siblings('[name="title"]').val();
    if( title == ""){
      alert("Title cannot be empty.");
      return;
    }
    var details = $(this).siblings('[name="details"]').val();
    if( details == ""){
      alert("Title cannot be empty.");
      return;
    }

    $.ajax({
      url: '/new_ad/',
      type: 'POST',
      data: { title : title,
              details: details,
              skills : JSON.stringify(skills_val),
            },

      success: function(json){
        alert("success");
      },

      error: function(){
        alert("error");
      }
    });

  });
});

//add new skill to ad button
$(document).ready(function() {
  $('.add_skill').click(function(event) {
    event.preventDefault();
    $(this).before('<input class="form-control skill" type="text" name="skill" placeholder="Add a skill">');
  });
});

//apply for an ad
$(document).ready(function() {
  $('.ad_apply').click(function(event) {
    event.preventDefault();
    var element = $(this);

    $.ajax({
      url: '/ad_apply/',
      type: 'POST',
      data: { ad_id: $(this).val(),},

      success: function(json){
        $(element).closest(".post-actions").replaceWith("already applied");
        console.log(json.message);
      },

      error: function(){
        alert("error");
      }
    });

  });
});


/****************profile.html related******************************************/
//add new skill to profile button
$('.skill_plus').click(function(event) {
  $(this).before('<input class="form-control skill" type="text" name="skill" placeholder="Add a skill">');
});
