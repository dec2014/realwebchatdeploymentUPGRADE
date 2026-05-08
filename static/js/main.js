

let chatName=''
let chatSocket=null
let chatWindow=window.location.href





const user_id=document.querySelector('#user_id').textContent.replaceAll('"',"")
const user_name=document.querySelector('#user_name').textContent.replaceAll('"',"")
const user={
    id:user_id,
    name:user_name
};
console.log(user)
const chatElemnet=document.querySelector('#chat')
const chatOpenElemnet=document.querySelector('#chat_open')
const chatJoinElemnet=document.querySelector('#chat_join')
const chatIconElemnet=document.querySelector('#chat_icon')
const chatWelcomeElemnet=document.querySelector('#chat_welcome')
const chatRoomElemnet=document.querySelector('#chat_room')
const chatNameElemnet=document.querySelector('#chat_name')
const chatLogElemnet=document.querySelector('#chat_log')
const chatMessageElemnet=document.querySelector('#chat_message_input')
const chatSubmitElemnet=document.querySelector('#chat_message_submit')

console.log(user_name)
function getCookie(name){
    var cookieValue=null
    if (document.cookie && document.cookie!=''){
        cookies=document.cookie.split(';')
        for (var i = 0; i<cookies.length; i++){
            var cookie=cookies[i].trim()
            if (cookie.substring(0,name.length+1) === (name + '=')){
                cookieValue=decodeURIComponent(cookie.substring(name.length+1))
                return cookieValue
            }
        }
    }
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type':'message',
        'body':chatMessageElemnet.value,
        'room':chat_name,

    }))
    chatMessageElemnet.value=''
}


function onChatMesssage(data){
    console.log(data)
    const userBubble = `
    <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
        <div>
            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg shadow-sm">
                <p class="text-sm">
                    ${data.message}
                </p>
            </div>
            <div class="flex justify-end items-center mt-1 space-x-1">
                <span class="text-[10px] text-gray-400 uppercase font-semibold">
                    ${data.created_at} ago
                </span>
            </div>
        </div>
        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold shadow-inner">
            ${data.initials}
        </div>
    </div>
`;

    // This represents a message received from another user (aligned to the left)
    const guestBubble = `
        <div class="flex w-full mt-2 space-x-3 max-w-md">
            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-400 text-white flex items-center justify-center font-bold shadow-inner">
                ${data.initials}
            </div>
            <div>
                <div class="bg-gray-200 text-gray-800 p-3 rounded-r-lg rounded-bl-lg shadow-sm">
                    <p class="text-sm">
                        ${data.message}
                    </p>
                </div>
                <div class="flex justify-start items-center mt-1 space-x-1">
                    <span class="text-[10px] text-gray-500 uppercase font-semibold">
                        ${data.created_at}
                    </span>
                </div>
            </div>
        </div>
    `;


    if (data.type=='chat_message'){

        if (data.created_by_id!=user_id){
            chatLogElemnet.innerHTML+=guestBubble

        }else{
            chatLogElemnet.innerHTML+=userBubble
        }
    }

}
// This represents a message sent by the current user (aligned to the right)



async function JoinChatRoom(){

    chat_name=chatNameElemnet.value
    console.log(chat_name)
    

    await fetch(`http://127.0.0.1:8000/create-room/${chat_name}/`,{
        method:'POST',
        headers:{
            'X-CSRFToken':getCookie('csrftoken')

        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        console.log('data',data)
    })

    chatSocket=new WebSocket(`wss://${window.location.host}/ws/${chat_name}/`)
    chatSocket.onmessage=function(e){
        console.log('onMessage')

        onChatMesssage(JSON.parse(e.data))
    }
    chatSocket.onclose=function(e){
        console.log('onclose')
    }
    chatSocket.onopen=function(e){
        console.log('onOpen')
    }

}


chatOpenElemnet.onclick = function(e){
    e.preventDefault()
    chatIconElemnet.classList.add('hidden')
    chatWelcomeElemnet.classList.remove('hidden')
    return false
}



chatJoinElemnet.onclick = function(e){
    e.preventDefault()
    chatWelcomeElemnet.classList.add('hidden')
    chatRoomElemnet.classList.remove('hidden')

    JoinChatRoom()
    return false
    
}

chatSubmitElemnet.onclick=function(e){
    sendMessage()
    return false
}
