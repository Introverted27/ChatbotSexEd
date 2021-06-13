var $messages = $('.messages-content'),
    d, h, m;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    botReply();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}
var currentMsg = null
function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  currentMsg = msg
  $('.message-input').val(null);
  updateScrollbar();

  botReply();
  console.log(currentMsg)
  currentMsg = null
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})



function botReply() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  $('.message.loading').remove();

  var host = window.location.hostname
  var port = window.location.port
  var url = "http://" + host + ":" + port + "/api/reply?q=" + currentMsg

  console.log(url)

  var reply = null
  $.getJSON(url, function(data) {
      //data is the JSON string
      $('<div class="message new"><figure class="avatar"><img src="" /></figure>' + data + '</div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      updateScrollbar();
      console.log(data)
  });



}
