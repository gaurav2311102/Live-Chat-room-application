const roomName = JSON.parse(document.getElementById('room-name').textContent)
const currentUser = JSON.parse(document.getElementById('logged-user').textContent)

var ws = new WebSocket(
    'ws://' + 
    window.location.host +  
    '/ws/ac/' + 
    roomName + 
    '/'
)

ws.onopen = function(){
    console.log("websocket connection open...")
    
}

ws.onmessage =  function(event){
 
    var data = JSON.parse(event.data)

    console.log("DATA ", data)
    console.log("type of data : ", data.type);



    if (data.type === 'message_add'){
        
        var is_Admin = data['is_Admin']
        var messagebox = document.createElement("div")
        if (data.user === currentUser) {
            messagebox.classList.add("message-box-self")
            messagebox.id = `message-${data.msg_id}`;
            
        }
        
        else{
            messagebox.classList.add("message-box-other")
            messagebox.id = `message-${data.msg_id}`;
        }
    
        // var messageContent = document.createElement("div");
        // messageContent.classList.add("message-content");
        
        var messageLine = document.createElement("span")
        messageLine.classList.add("message-line")

        var messageSpan = document.createElement("span");
       
        if (data.deleted) {    
            messageSpan.innerHTML = "<span class='deleted-or-edited-message'>This message was deleted </span>"        
        }
        else{
                messageSpan.innerText = `${data.msg}  `
            }  

        messageSpan.classList.add("message-text");
        
        var timescince = document.createElement('span');
        timescince.innerText = `(${data.created})`;
        timescince.classList.add('message-time')
    
       
        var userSmall = document.createElement("small");
        userSmall.classList.add('message-title')
        userSmall.innerHTML = `<strong>${data.user}</strong> `;
        if (data.edited) {
            userSmall.innerHTML += "<p class='deleted-or-edited-message'> Edited </p>";
        }
          
        
        let modifydivcontainer = document.createElement("div");
        modifydivcontainer.classList.add("modify-div-container")

        let modifyDiv = document.createElement("div");
        modifyDiv.classList.add("message-modify");
    
        if (data.deleted === false){

            if (data.user === currentUser || is_Admin) {  
                let actionsDiv = document.createElement("div");
                actionsDiv.classList.add("message-actions");
        
                
                if (data.user === currentUser) {
                    
                    let edit_button = document.createElement("button");
                    edit_button.innerHTML = '<i class="fas fa-edit"></i>';
                    edit_button.classList.add("edit-icon");

                    edit_button.onclick = function() {
                        const currentText = messageSpan.innerText;
                        editMessage(data.msg_id, currentText);
                    }
                
                    
                    let delete_button = document.createElement("button");
                    delete_button.innerHTML = '<i class="bi bi-trash"></i>';
                    delete_button.classList.add('delete-icon')
                    delete_button.onclick = function(){
                        confirmDelete( data.msg_id);
                    }

                    actionsDiv.appendChild(edit_button);
                    actionsDiv.appendChild(delete_button);
                }

                modifyDiv.appendChild(actionsDiv);
            }
        }

        messageLine.appendChild(messageSpan);
        messageLine.appendChild(timescince); 
        
        modifydivcontainer.appendChild(modifyDiv)
        messagebox.appendChild(modifydivcontainer);
        messagebox.appendChild(userSmall);
        messagebox.appendChild(messageLine); 
        
        
    
        document.querySelector(".message-container-top").appendChild(messagebox); 
        scrollToBottom() 
    
    }
    
    else if (data.type === "message_update") {
        const messageId = data.msg_id;
        const newText = data.new_text;
        
        const messageElement = document.getElementById(`message-${messageId}`);
        if (messageElement) {
            const messageText = messageElement.querySelector('.message-text');
            messageText.innerText = newText;

            const messageTitle = messageElement.querySelector('.message-title')
            messageTitle.innerHTML += "<p class='deleted-or-edited-message'> Edited </p>";

        }
    }

    else if (data.type === 'message_delete'){
        
        const messageId = data.msg_id;
        const messageElement = document.getElementById(`message-${messageId}`);
        if (messageElement) {
           
            messageElement.querySelector('.message-text').innerHTML = "<span class='deleted-message'>This message was deleted</span>  ";

            const deleteIcon = messageElement.querySelector('.delete-icon');
            if (deleteIcon) {
                deleteIcon.style.display = 'none';
            }
            const editIcon = messageElement.querySelector('.edit-icon');
            if(editIcon){
                editIcon.style.display = 'none';
            }
        }

    }   

}

ws.onerror =  function(event){
    console.log("error occured", event)
}

ws.onclose =  function(event){
    console.log("websocket closed....", event)
}


function scrollToBottom() {
    let messageContainer = document.querySelector(".message-container-top");
    messageContainer.scrollTo({ top: messageContainer.scrollHeight, behavior: "smooth" });
}


document.getElementById("message-form").onsubmit = function (event) {
    event.preventDefault();
    const messageInputDom = document.getElementsByClassName("message-input")[0];
    const message = messageInputDom.value.trim();

    if (message.length > 0) {
        
        ws.send(JSON.stringify({'type': 'send_message', msg: message }));
        messageInputDom.value = ""; 
    }
};

function confirmDelete(messageId) {
    const confirmed = confirm("Are you sure you want to delete this message?");
    
    if (confirmed) {

        ws.send(JSON.stringify({
            type: 'delete_message',
            message_id : messageId,
        }));
    }
}

function editMessage(messageId, currentText) {
    const newText = prompt("Edit your message:", currentText);
    if (newText !== null && newText.trim() !== "") {
        ws.send(JSON.stringify({
            type: "update_message",
            message_id: messageId,
            new_text: newText.trim()
        }));
    }
}
