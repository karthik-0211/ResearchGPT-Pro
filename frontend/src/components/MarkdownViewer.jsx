import ReactMarkdown

from "react-markdown"

import remarkGfm

from "remark-gfm"



function MarkdownViewer({

content

}){


return(

<ReactMarkdown

remarkPlugins={[

remarkGfm

]}

>

{content}

</ReactMarkdown>

)

}


export default MarkdownViewer