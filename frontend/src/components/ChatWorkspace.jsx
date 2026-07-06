import { useState, useRef, useEffect } from "react";

import MarkdownViewer from "./MarkdownViewer";
import { API_BASE_URL } from "../config";

export default function ChatWorkspace({

  messages,

  setMessages,

  sessionId,

  setSessionId

}) {

const [query,setQuery]=useState("");

const [file,setFile]=useState(null);

const [loading,setLoading]=useState(false);

const bottomRef=useRef();




useEffect(()=>{

bottomRef.current?.scrollIntoView({

behavior:"smooth"

});

},[messages,loading]);






const copyText=(text)=>{

navigator.clipboard.writeText(text);

};








const sendResearch=async()=>{


if(!query.trim() && !file) return;



const userQuery=query.trim() || "Summarize this file";



setQuery("");



setMessages(prev=>[

...prev,

{

role:"user",

content: query.trim(),

file_name: file ? file.name : null

}

]);



setLoading(true);






const formData=new FormData();


formData.append(

"query",

userQuery

);



if(sessionId){

formData.append(

"session_id",

sessionId

)

}



if(file){

formData.append(

"file",

file

)

}








try{


const response=await fetch(

`${API_BASE_URL}/research`,

{

method:"POST",

body:formData

}

);





/* SAVE SESSION */

const newSessionId=

response.headers.get("X-Session-Id") || response.headers.get("x-session-id");



if(

newSessionId

&&

!sessionId

){

setSessionId(

newSessionId

)

}








const reader=response.body.getReader();

const decoder=new TextDecoder();



let assistantText="";





setMessages(prev=>[

...prev,

{

role:"assistant",

content:""

}

]);








while(true){


const {

done,

value

}=await reader.read();



if(done) break;





const chunk=

decoder.decode(value);





/* REMOVE AGENT EVENTS */

const cleanedChunk=

chunk

.replace(/\[AGENT\].*/g,"");





if(cleanedChunk===""){

continue;

}






assistantText+=

cleanedChunk;








if(

assistantText.trimStart()!==""


){

setMessages(prev=>{


const arr=[...prev];



arr[arr.length-1]={

role:"assistant",

content:

assistantText.trimStart()

};



return arr;


});

}


}




}

catch(e){


console.log(e);



setMessages(prev=>[

...prev,

{

role:"assistant",

content:

"I don't have enough reliable information to answer this."

}

]);



}



setLoading(false);

setFile(null);



}









return(


<div className="chat-container">



<div className="messages">



{

messages.length===0 &&

<div className="welcome">

ResearchGPT

</div>

}








{

messages.map((m,i)=>(


<div

key={i}

className="message-block"

>




<div

className={

m.role==="user"

?

"user"

:

"assistant"

}

>

{m.role === "user" ? (

  <div className="user-msg-content">

    {m.file_name && (

      <div className="msg-file-badge">

        <span className="msg-file-icon">📄</span>

        <span className="msg-file-name" title={m.file_name}>{m.file_name}</span>

      </div>

    )}

    {m.content && <div className="msg-text">{m.content}</div>}

  </div>

) : (

  <MarkdownViewer content={m.content} />

)}

</div>








<div className="message-actions">


<button

className="icon-btn"

title="Copy"

onClick={()=>

copyText(

m.content

)

}

>

⧉

</button>


</div>





</div>

))

}









{

loading &&

<div className="thinking">


<div className="dots">

<span></span>

<span></span>

<span></span>

</div>


Thinking...


</div>

}






<div ref={bottomRef}></div>



</div>









<div className="input-area">



<label className="upload-btn">

＋


<input

hidden

type="file"

accept=".pdf,.docx,.doc,.pptx,.ppt,.txt,.csv,.md"

onClick={(e) => { e.target.value = null; }}

onChange={(e)=>

setFile(

e.target.files[0]

)

}

/>

</label>







{

file &&

<div className="file-badge">

<span className="file-name" title={file.name}>{file.name}</span>

<button type="button" className="remove-btn" onClick={() => setFile(null)} title="Remove file">×</button>

</div>

}








<input

className="chat-input"

placeholder="Ask anything..."

value={query}



onChange={(e)=>

setQuery(

e.target.value

)

}



onKeyDown={(e)=>{

if(e.key==="Enter"){

sendResearch()

}

}}


/>








<button

className="research-btn"

onClick={sendResearch}

>

Send

</button>





</div>




</div>

)

}