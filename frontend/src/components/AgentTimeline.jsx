function AgentTimeline({

agents

}){


return(

<div className="timeline">


{

agents.map(

(a,index)=>(

<div

key={index}

className="agent-item"

>

{

a.status==="running"

?

"●"

:

"✓"

}

{" "}

{a.agent}

-

{a.status}

</div>

)

)

}


</div>

)

}


export default AgentTimeline