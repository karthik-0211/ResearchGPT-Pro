function ChatMessage({

role,

children

}){


return(

<div

className={

role==="user"

?

"user-message"

:

"assistant-message"

}

>

{children}

</div>

)

}


export default ChatMessage