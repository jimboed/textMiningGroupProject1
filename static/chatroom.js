(function(n,e){
    var socket=io();
    var o=$(".chatwindow");
    var t=o.attr("room-key");
    var s=o.attr("viewer-id");
    $("#join-form").on("submit",function(n) {
        n.preventDefault();
        var e=$("#join-nick").val();
        if(e){
            console.log("joining room %s as %s",t,e);
            socket.emit("enterchat",{sid:s,room:t,name:e});
            console.log("tried to join")
        }
    }
    );
    $("#chat-input").on("submit",function(n){
        n.preventDefault();
        var e=$("#in-msg").val().trim();
        if(!e)return;console.log("submitting message");
        socket.emit("chat",{sid:s,room:t,message:e});
        $("#in-msg").val("")}
    );
    socket.on("connect",function(){
        console.log("connected");
        var n=o.attr("viewer-name");
        if(n){console.log("re-joining room %s", t);
            socket.emit("enterchat",{sid:s,room:t,name:n})
        }
    });
    socket.on("joined",function(n) {
        var e=n.name;
        console.log("joined %s as %s", t, e);
        o.attr("data-nick", e);
        o.addClass("joined");
        o.removeClass("unjoined");
    }
    );
    socket.on("new-chat",function(n){
        $("<li>").addClass("message").append($("<span>").addClass("user").text(n.sender)).append(": ").append($("<span>").addClass("text").text(n.message)).appendTo($(".chat-messages"))}
    );
    socket.on("user-joined",function(n){
        $("<li>").addClass("joined").append($("<span>").addClass("user").text(n.name)).append(" has joined the chat").appendTo($(".chat-messages"));
        $("<li>").text(n.name).appendTo($(".roster-list"))}
    );
    e[""]=n
})
({},function(){
    return this
}()
);
