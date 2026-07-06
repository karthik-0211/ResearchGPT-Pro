import { useEffect, useState } from "react";
import { API_BASE_URL } from "../config";

export default function SessionHistory({

  setMessages,

  sessionId,

  setSessionId

}) {


const [sessions,setSessions]=useState([]);





const fetchSessions=async()=>{

try{

const response=await fetch(

`${API_BASE_URL}/sessions`

);


const data=await response.json();



if(Array.isArray(data)){

setSessions(data);

}

else{

setSessions([]);

}


}

catch(err){

console.log(err);

setSessions([]);

}

};






useEffect(()=>{

fetchSessions();




const interval=setInterval(

fetchSessions,

5000

);




return()=>clearInterval(interval);


},[sessionId]);









const loadSession=async(id)=>{


try{


const response=await fetch(

`${API_BASE_URL}/session/${id}`

);


const data=await response.json();




const cleanedMessages=(

data.messages || []

).map(msg=>({

role:msg.role,

content:

(msg.content || "")

.trim()

}));




setMessages(

cleanedMessages

);



setSessionId(

id

);



}

catch(err){

console.log(err);

}


};









const PinIcon = ({ pinned }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 24 24" 
    fill={pinned ? "#10A37F" : "none"} 
    stroke={pinned ? "#10A37F" : "currentColor"} 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    style={{ width: "14px", height: "14px" }}
  >
    <line x1="12" y1="17" x2="12" y2="22"></line>
    <path d="M5 17h14v-1.76a2 2 0 0 0-.44-1.24l-2.33-2.92A2 2 0 0 1 15.8 9.84V5a2 2 0 0 0-2-2h-3.6a2 2 0 0 0-2 2v4.84a2 2 0 0 1-.43 1.24l-2.33 2.92a2 2 0 0 0-.44 1.24z"></path>
  </svg>
);

const deleteSession=async(e,id)=>{
  e.stopPropagation();
  const ok=window.confirm("Delete this chat?");
  if(!ok) return;

  try{
    await fetch(`${API_BASE_URL}/session/${id}`, {
      method:"DELETE"
    });
    setSessions(prev=>prev.filter(s=>s.id!==id));
    window.dispatchEvent(new Event("reports-updated"));
  }
  catch(err){
    console.log(err);
  }
};

const togglePin=async(e,id,pinned)=>{
  e.stopPropagation();
  try{
    const response=await fetch(`${API_BASE_URL}/session/${id}/pin?pinned=${pinned}`, {
      method:"POST"
    });
    if(response.ok){
      setSessions(prev=>prev.map(s=>s.id===id ? { ...s, pinned } : s));
      window.dispatchEvent(new Event("reports-updated"));
    }
  }
  catch(err){
    console.log(err);
  }
};;









  const pinnedSessions = sessions.filter(s => s.pinned);
  const recentSessions = sessions.filter(s => !s.pinned);

  const renderSessionCard = (s) => (
    <div
      key={s.id}
      className={`session-card ${s.id === sessionId ? "active-session" : ""}`}
      onClick={() => loadSession(s.id)}
    >
      <div className="session-title">
        {s.title.length > 35 ? s.title.slice(0, 35) + "..." : s.title}
      </div>
      <div className="session-actions">
        <button
          className={`session-pin ${s.pinned ? "active" : ""}`}
          title={s.pinned ? "Unpin" : "Pin"}
          onClick={(e) => togglePin(e, s.id, !s.pinned)}
        >
          <PinIcon pinned={s.pinned} />
        </button>
        <button
          className="session-delete"
          title="Delete"
          onClick={(e) => deleteSession(e, s.id)}
        >
          ✕
        </button>
      </div>
    </div>
  );

  return (
    <div className="section">
      {pinnedSessions.length > 0 && (
        <div className="pinned-chats-section">
          <h3>📌 Pinned</h3>
          {pinnedSessions.map(renderSessionCard)}
        </div>
      )}

      <h3>Recent Chats</h3>
      {recentSessions.length === 0 ? (
        pinnedSessions.length === 0 ? (
          <div className="empty-text">No Chats Yet</div>
        ) : null
      ) : (
        recentSessions.map(renderSessionCard)
      )}
    </div>
  );

}