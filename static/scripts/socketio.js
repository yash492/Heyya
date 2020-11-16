document.addEventListener('DOMContentLoaded', () =>{
    var socket = io();
    let room = "room";
    joinRoom("room")


    // Incoming messages
    socket.on('message', data => {
        // Display current message
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')
            // Display user's own message
            if (data.username == username) {
                    p.setAttribute("class", "my-msg");

                    // Username
                    span_username.setAttribute("class", "my-username");
                    span_username.innerText = data.username;

                    // Timestamp
                    span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML to append
                    p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

                    //Append
                    document.querySelector('#display-message-section').append(p);
            }
            // Display other users' messages
            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

                //Append
                document.querySelector('#display-message-section').append(p);
            }
            // Display system message
            else {
                printSysMsg(data.msg);
            }


        }
    });

    //Send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg' : document.querySelector('#user_message').value, 'username': username, 'room': room});
        document.querySelector('#user_message').value = ''
    }

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room' : room});
        //Clear message area
        document.querySelector('#display-message-section').innerHTML = ''
        document.querySelector('#user_message').focus();
    }

    function leaveRoom(room) {
        socket.emit('leave', {'username': name, 'room' : room});
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);

    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
});
