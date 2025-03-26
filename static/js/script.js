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
    var is_Admin = data['is_Admin']
    var messagebox = document.createElement("div")
    if (data.user === currentUser) {
        messagebox.classList.add("message-box-self")
    }
    else{
        messagebox.classList.add("message-box-other")
    }

    var messageContent = document.createElement("div");
    messageContent.classList.add("message-content");

    var messageSpan = document.createElement("span");
    messageSpan.innerText = `${data.msg}  `; 
    messageSpan.classList.add("message-text");
    
    var timescince = document.createElement('span');
    timescince.innerText = `(${data.updated})`;
    timescince.classList.add('message-time')

   
    var userSmall = document.createElement("small");
    userSmall.innerHTML = `<strong>${data.user}</strong> `; 


    let modifyDiv = document.createElement("div");
    modifyDiv.classList.add("message-modify");

 
    if (data.user === currentUser || is_Admin) {  
        let actionsDiv = document.createElement("div");
        actionsDiv.classList.add("message-actions");

        
        if (data.user === currentUser) {
            let editLink = document.createElement("a");
            editLink.href = `/update-message/${data['msg_id']}/`;  
            editLink.classList.add("edit-icon");
            editLink.innerHTML = `<i class="fas fa-edit"></i>`;
            actionsDiv.appendChild(editLink);
        }

        
        let deleteLink = document.createElement("a");
        deleteLink.href = `/delete-message/${data['msg_id']}/`;  
        deleteLink.classList.add("delete-icon");
        deleteLink.innerHTML = `<i class="bi bi-trash"></i>`;
        
        actionsDiv.appendChild(deleteLink);

        modifyDiv.appendChild(actionsDiv);
    }

    messageContent.appendChild(userSmall);
    messageContent.appendChild(document.createElement('br'));
    messageContent.appendChild(messageSpan); 
    messageContent.appendChild(timescince); 
    
    
    
    messagebox.appendChild(messageContent)
    messagebox.appendChild(modifyDiv);

    document.querySelector(".message-container-top").appendChild(messagebox); 
    scrollToBottom() 

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
    const messageInputDom = document.getElementById("message-input");
    const message = messageInputDom.value.trim();

    if (message.length > 0) {
        
        ws.send(JSON.stringify({ msg: message }));
        messageInputDom.value = ""; 
    }
};