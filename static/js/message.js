$(document).on('submit', '#message-form', function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/send_message',
    data: {
      username: $('#username').val(),
      room: $('#room').val(),
      message: $('#message').val(),
      csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken]').val()
    }
  })
})

$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: "../../get_message/{{username}}",
    success: function (response) {
      
      $('#message_cont').empty()
      
    }
  })

})


// {% for message in messages%}
        
//         {% if message.sender.username == request.user.username %}


        
          
//         {% else %}
        '<div class="flex gap-sm margin__top__lg">{% if current_sender_friend %}<img src="{{current_sender_friend.sender_profile.profile.url}}" alt="" class="profile__msg_img" />{% else %}<img src="{{current_receiver_friend.receiver_profile.profile.url}}" alt="" class="profile__msg_img" />{% endif %}<div class="receive__message"><p>'+message.value+'</p></div></div>'
//         {% endif %}
          
//         {% endfor %}