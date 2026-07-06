import SessionHistory from "./SessionHistory";
import SavedReports from "./SavedReports";



export default function Sidebar({

  setMessages,

  sessionId,

  setSessionId

}) {



  const newChat = () => {

    setMessages([]);

    setSessionId(null);

  };




  return (

    <div className="sidebar">


      {/* Logo */}

      <div className="logo">

        <div className="logo-icon">

          RG

        </div>


        <div className="logo-text">

          ResearchGPT

          <span> Pro</span>

        </div>

      </div>





      {/* New Chat */}

      <button

        className="new-btn"

        onClick={newChat}

      >

        + New Chat

      </button>






      {/* Session History */}

      <div className="sidebar-section">

        <SessionHistory

          setMessages={setMessages}

          sessionId={sessionId}

          setSessionId={setSessionId}

        />

      </div>






      {/* Saved Reports */}

      <div className="sidebar-section">

        <SavedReports />

      </div>







      {/* Footer */}

      <div className="sidebar-footer">

        ResearchGPT Pro


        <div className="footer-sub">

          AI Research Assistant

        </div>

      </div>



    </div>

  );

}