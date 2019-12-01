//var socket = io();

function scrollChat() {
    // a jQuery result is a list, get the first element
    var chat = $('#messages')[0];
    // figure out the height the *top* of window should scroll to
    var pos = chat.scrollHeight - chat.clientHeight;
    chat.scrollTop = pos;
}



/* Listen to new chats on the form */
$('#eliza-chat').on('submit', function(event) {
    // don't really submit the form
    // we handle in JS, a real submit would reload page (sad)
    event.preventDefault();
    // get the message - it's the value of the message element
    var msg = $('#m').val();
    // send the message to the server
    socket.send(msg);
    // reset the message input
    $('#m').val('');
    // add the message to the end of our list
    // most jQuery operations return the 'jquery' object they were
    // called on
    /* This says:
       Append to '#messages' the results of
       1. building an 'li' element
       2. adding 'sent' to its 'class' attribute
       3. setting its text to the message content
     */
    $('#messages').append($('<div>').addClass('sent').text(msg));
   // $('#messages').append(sendTmpl);
    scrollChat();
});

/* listen for replies */
socket.on('message', function(msg) {
    // add it to the list!
    $('#messages').append($('<div>').addClass('received').text(msg));
    scrollChat();
});
