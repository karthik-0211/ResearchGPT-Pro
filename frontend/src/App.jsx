import { useState } from "react";

import Sidebar from "./components/Sidebar";
import ChatWorkspace from "./components/ChatWorkspace";

import "./index.css";



export default function App() {

  const [messages, setMessages] = useState([]);

  const [sessionId, setSessionId] = useState(null);



  return (

    <div className="app">

      <Sidebar

        setMessages={setMessages}

        sessionId={sessionId}

        setSessionId={setSessionId}

      />



      <ChatWorkspace

        messages={messages}

        setMessages={setMessages}

        sessionId={sessionId}

        setSessionId={setSessionId}

      />


    </div>

  );

}