function FileUpload({

setFile

}){


return(

<input

type="file"

accept=".pdf"

onChange={(e)=>

setFile(

e.target.files[0]

)

}

/>

)

}


export default FileUpload