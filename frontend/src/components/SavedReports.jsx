import { useEffect, useState } from "react";
import { API_BASE_URL } from "../config";

export default function SavedReports() {

const [reports,setReports]=useState([]);

const [search,setSearch]=useState("");





const fetchReports=async()=>{

try{

const response=await fetch(

`${API_BASE_URL}/reports`

);

const data=await response.json();



if(Array.isArray(data)){

setReports(

[...data].reverse()

);

}

else{

setReports([]);

}

}

catch(err){

console.log(err);

setReports([]);

}

};






useEffect(()=>{

fetchReports();



const handleUpdate=()=>{

fetchReports();

};



window.addEventListener("reports-updated", handleUpdate);



return()=>{

window.removeEventListener("reports-updated", handleUpdate);

};

},[]);








const deleteReport=async(e,id)=>{


e.stopPropagation();


const ok=window.confirm(

"Delete this report permanently?"

);


if(!ok) return;



try{


await fetch(

`${API_BASE_URL}/report/${id}`,

{

method:"DELETE"

}

);


fetchReports();

}

catch(err){

console.log(err);

}

};











const copyReport=(e,text)=>{


e.stopPropagation();


navigator.clipboard.writeText(text);


};



//////// OPEN REPORT ////////

const openReport=async(id)=>{


try{


const response=await fetch(

`${API_BASE_URL}/report/${id}`

);


const data=await response.json();



const win=window.open(

"",

"_blank"

);



if(!win){

alert("Allow popups");

return;

}



win.document.write(`

<html>

<head>

<title>${data.title}</title>

<style>

body{

background:#212121;

color:#ECECEC;

font-family:Inter,sans-serif;

padding:60px;

max-width:900px;

margin:auto;

line-height:1.9;

font-size:16px;

}

h1{

color:#10a37f;

margin-bottom:25px;

font-size:32px;

}

h2, h3, h4 {

color: #ECECEC;

margin-top: 30px;

margin-bottom: 15px;

}

hr{

border:0;

height:1px;

background:#333;

margin-bottom:25px;

}

p {

margin-bottom: 20px;

}

ul, ol {

margin-bottom: 20px;

padding-left: 20px;

}

li {

margin-bottom: 8px;

}

code {

background: #2d2d2d;

padding: 2px 6px;

border-radius: 4px;

font-family: monospace;

}

pre {

background: #2d2d2d;

padding: 15px;

border-radius: 6px;

overflow-x: auto;

margin-bottom: 20px;

}

pre code {

padding: 0;

background: none;

}

table {

border-collapse: collapse;

width: 100%;

margin-bottom: 20px;

}

th, td {

border: 1px solid #333;

padding: 10px 15px;

text-align: left;

}

th {

background: #2d2d2d;

}

</style>

</head>

<body>

<h1>

${data.title}

</h1>

<hr>

<div id="content-area">Loading report...</div>

<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<script>

  document.addEventListener('DOMContentLoaded', () => {

    const rawContent = ${JSON.stringify(data.content)};

    document.getElementById('content-area').innerHTML = marked.parse(rawContent);

  });

</script>

</body>

</html>

`);


win.document.close();

}

catch(err){

console.log(err);

}

};









const filtered=reports.filter(r=>

r.title

.toLowerCase()

.includes(

search.toLowerCase()

)

);











return(


<div className="section">


<h3>

Saved Reports ({filtered.length})

</h3>






<input

className="report-search"

placeholder="Search reports..."

value={search}

onChange={(e)=>

setSearch(

e.target.value

)

}

/>








{

filtered.length===0

?

<div className="empty-text">

📄 No Saved Reports

</div>

:

filtered.map((r)=>(


<div

key={r.id}

className="saved-card"

onClick={()=>

openReport(r.id)

}

>





<div className="saved-title">

{r.title}

</div>






<div className="saved-actions">





<button

className="mini-btn"

title="Copy"

onClick={(e)=>

copyReport(

e,

r.content

)

}

>

⧉

</button>






<button

className="mini-btn delete"

title="Delete"

onClick={(e)=>

deleteReport(

e,

r.id

)

}

>

✕

</button>






</div>





</div>

))

}



</div>

)

}