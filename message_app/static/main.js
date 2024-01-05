var contact_id = "";

function handleSearcher(clear = false) {
    input = document.getElementById('searcherInput');
    contacts = document.getElementsByClassName('contact');
    console.log(contacts[0].style.display);

    if (input.value == '' || clear) {
        for (i = 0; i < contacts.length; i++) {
            contacts[i].style.display = 'flex';
        } return;
    }

    for (i = 0; i < contacts.length; i++) {
        if (contacts[i].innerHTML.toLowerCase().includes(input.value.toLowerCase())) {
            contacts[i].style.display = 'flex';
        } else {
            contacts[i].style.display = 'none';
        }
    }
}

function handleMessages() {
    function sendMessage() {
        input = document.getElementById('messageInput');
        messagesDiv = document.getElementById('messagesDiv');
        messagesBlock = document.getElementById('messageBlock');

        if (input.value == '') { return; }

        fetch('/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'message': messageInput.value,
                'senderID': senderID,
                'receiverID': contact_id,
            })
        }).catch(error => {
            alert('Error sending message');
            return;
        });

        newMessage = document.createElement('div');
        newMessage.className = 'messageDiv owner';

        text = document.createElement('p');
        text.innerHTML = input.value;

        newMessage.appendChild(text);
        messagesBlock.appendChild(newMessage);

        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        input.value = '';
    }

    const form = document.getElementById("messageInputDiv");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
    });
    form.addEventListener("submit", sendMessage);
}

function handleAddContact() {
    var allElements = document.querySelectorAll('body *');
    var wrapDiv = document.querySelector('.wrapper');
    wrapDiv.style.display = 'block';

    for (var i = 0; i < allElements.length; i++) {
        if (!wrapDiv.contains(allElements[i])) {
            allElements[i].style.filter = 'blur(3px)';
        }
    }

    setTimeout(function () {
        document.addEventListener('click', function (event) {
            var wrapDiv = document.querySelector('.wrapper');
            if (!wrapDiv.contains(event.target)) {
                document.removeEventListener('click', arguments.callee);
                wrapDiv.style.display = 'none';
                for (var i = 0; i < allElements.length; i++) {
                    allElements[i].style.filter = 'blur(0px)';
                }
            }
        });
    }, 1000);
}

// <div class="messageDiv">
// <p>{{ message }}</p>
// </div>
function loadChat(id) {
    contact_id = id;
    rightDiv = document.getElementById('rightDiv');
    messagesDiv = document.getElementById('messagesDiv');
    input = document.getElementById('messageInputDiv');

    rightDiv.className = '';
    input.style.display = 'flex';
    messagesDiv.style.display = 'block';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    typewriter = document.getElementById('typewriter');
    if (typewriter) {
        typewriter.style.display = 'none';
    }

    messageBlock = document.getElementById('messageBlock');
    while (messageBlock.firstChild) {
        messageBlock.removeChild(messageBlock.firstChild);
    }

    fetch('messages/' + contact_id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
        .then(messages => {
            for (i = 0; i < messages.length; i++) {
                newMessage = document.createElement('div');
                newMessage.className = 'messageDiv';

                text = document.createElement('p');
                text.innerHTML = messages[i].message;

                newMessage.appendChild(text);
                messageBlock.appendChild(newMessage);
            }
        }).catch(error => {
            alert('Error loading messages');
            return;
        });
}