/**********************index.html related*************************************/
//submit a new post
$(document).ready(function() {
  $('.post_submit').click(function(event) {
    event.preventDefault();
    var element = $(this);
    var status = $(this).siblings('[name="status"]').val();
    if( status == ""){
      alert("write something.");
      return;
    }

    $.ajax({
      url: '/post_submit/',
      type: 'POST',
      data: { status: status,
              csrfmiddlewaretoken: getCookie('csrftoken'),},

      success: function(data){
        $(element).closest("form").closest(".panel-body").closest(".panel").after(data);
      },

      error: function(){
        alert("error");
      }
    });

  });
});

//make a new comment
//(this event had to be delegated all the way up to col-md-8, othervise when
//creating a new post dynamically it would not trigger the even for its comment submit form)
$(document).ready(function() {
  $('.col-md-8').on('click','.comment_submit', function(event) {
    event.preventDefault();
    var element = $(this);
    var comment = $(this).siblings('[name="comment"]').val();
    var post_id = $(this).val();
    if( comment == ""){
      return;
    }

    $.ajax({
      url: '/comment_submit/',
      type: 'POST',
      data: { comment: comment,
              post_id: post_id,
              csrfmiddlewaretoken: getCookie('csrftoken'),},

      success: function(data){
        $(element).closest("form").closest(".comment-form").siblings(".comments").append(data);
      },

      error: function(){
        alert("error");
      }
    });

  });
});

//interest jquery for index.html
$(document).ready(function() {
    $('.col-md-8').on('click','.post_interested', function(event) {
        event.preventDefault();
        var element=$(this);
        var pid=$(element).attr("data-postid");

        $.ajax({
          url: '/interest/',
          type: 'POST',
          data: { postid: pid,
                  csrfmiddlewaretoken: getCookie('csrftoken'), },

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
              fr_id: $(element).val(),
              csrfmiddlewaretoken: getCookie('csrftoken'),},

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
              csrfmiddlewaretoken: getCookie('csrftoken'),},

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
    var element = $(this);
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
      alert("Details cannot be empty.");
      return;
    }

    $.ajax({
      url: '/new_ad/',
      type: 'POST',
      data: { title : title,
              details: details,
              skills : JSON.stringify(skills_val),
              csrfmiddlewaretoken: getCookie('csrftoken'),
            },

      success: function(data){
        $(element).closest("form").closest(".panel-body").closest(".panel").after(data);
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
      data: { ad_id: $(this).val(),
              csrfmiddlewaretoken: getCookie('csrftoken'),},

      success: function(json){
        $(element).closest(".post-actions").replaceWith('<button type="button" class="btn btn-success disabled btn-block apply ad_apply" ><i class="fa fa-check"></i> Already Applied</button>');
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


/********* MICS *********************************************************/
//Acquiring the token by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
