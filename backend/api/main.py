import os
import json
import uuid
import time

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from workflows.graph import graph

from memory.chat_history import (
    create_session,
    save_message,
    get_session,
    get_all_sessions,
    delete_session,
    pin_session
)

from memory.redis_memory import redis_client



app = FastAPI(

    title="ResearchGPT Pro"

)



# ---------------- CORS ----------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

    expose_headers=["X-Session-Id", "x-session-id"]

)




# ---------------- Upload Folder ----------------

UPLOAD_DIR = "uploads"

os.makedirs(

    UPLOAD_DIR,

    exist_ok=True

)




# ---------------- Home ----------------

@app.get("/")

def home():

    return {

        "message":

        "ResearchGPT Pro Running"

    }




# ---------------- Sessions ----------------

@app.get("/sessions")

def sessions():

    return get_all_sessions()




@app.get("/session/{session_id}")

def load_session(session_id: str):

    return get_session(session_id)




@app.delete("/session/{session_id}")

def remove_session(session_id: str):

    delete_session(session_id)

    return {

        "status": "deleted"

    }




@app.post("/session/{session_id}/pin")

def toggle_pin(session_id: str, pinned: bool):

    pin_session(session_id, pinned)

    return {

        "status": "success",

        "pinned": pinned

    }






# ---------------- Reports ----------------

@app.get("/reports")

def reports():

    result = []

    keys = redis_client.keys("report:*")



    for key in keys:

        data = redis_client.get(key)

        if data:

            result.append(

                json.loads(data)

            )



    # Fetch pinned sessions as reports

    session_keys = redis_client.keys("session:*")

    for key in session_keys:

        raw = redis_client.get(key)

        if raw:

            session_data = json.loads(raw)

            if session_data.get("pinned", False):

                messages = session_data.get("messages", [])

                assistant_msgs = [m for m in messages if m["role"] == "assistant"]

                content = assistant_msgs[-1]["content"] if assistant_msgs else "No report generated yet."

                result.append({

                    "id": session_data["id"],

                    "title": session_data["title"] + " (Pinned Chat)",

                    "content": content,

                    "is_pinned_chat": True

                })



    return result






@app.get("/report/{report_id}")

def report(report_id: str):

    data = redis_client.get(

        f"report:{report_id}"

    )


    if data:

        return json.loads(data)


    session_data = redis_client.get(f"session:{report_id}")

    if session_data:

        data = json.loads(session_data)

        messages = data.get("messages", [])

        assistant_msgs = [m for m in messages if m["role"] == "assistant"]

        content = assistant_msgs[-1]["content"] if assistant_msgs else "No report generated yet."

        return {

            "id": data["id"],

            "title": data["title"] + " (Pinned Chat)",

            "content": content,

            "is_pinned_chat": True

        }



    return {}






@app.delete("/report/{report_id}")

def delete_report(report_id: str):

    if redis_client.exists(f"report:{report_id}"):

        redis_client.delete(

            f"report:{report_id}"

        )

        return {

            "status": "deleted"

        }



    session_data = redis_client.get(f"session:{report_id}")

    if session_data:

        data = json.loads(session_data)

        data["pinned"] = False

        redis_client.set(f"session:{report_id}", json.dumps(data))

        return {

            "status": "unpinned"

        }



    return {

        "status": "not_found"

    }







@app.post("/save-report")

def save_report(

    title: str = Form(...),

    content: str = Form(...)

):


    report_id = str(

        uuid.uuid4()

    )



    redis_client.set(

        f"report:{report_id}",

        json.dumps({

            "id": report_id,

            "title": title,

            "content": content

        })

    )



    return {

        "status": "saved"

    }








# ---------------- RESEARCH ----------------

@app.post("/research")

async def research(

    query: str = Form(...),

    file: UploadFile = File(None),

    session_id: str = Form(None)

):



    if not session_id:

        session_id = create_session(

            query

        )



    session_data = get_session(session_id)

    history = session_data.get("messages", []) if session_data else []



    save_message(

        session_id,

        "user",

        query,

        file_name=file.filename if file else None

    )




    pdf_path = None



    if file:


        pdf_path = os.path.join(

            UPLOAD_DIR,

            file.filename

        )



        with open(

            pdf_path,

            "wb"

        ) as f:


            f.write(

                await file.read()

            )







    def generate():



        final_answer = ""



        try:



            result = graph.invoke({

                "query": query,

                "pdf_path": pdf_path,

                "session_id": session_id,

                "history": history

            })




            print("\n========== GRAPH OUTPUT ==========\n")

            print("RESEARCH NOTES:\n")

            print(result.get("research_notes"))


            print("\nSUMMARY:\n")

            print(result.get("summary"))


            print("\nFACTCHECK:\n")

            print(result.get("factcheck"))


            print("\nREPORT:\n")

            print(result.get("report"))


            print("\n=================================\n")





            report = result.get(

                "report",

                ""

            )


            factcheck = result.get(

                "factcheck",

                ""

            )


            summary = result.get(

                "summary",

                ""

            )


            research_notes = result.get(

                "research_notes",

                ""

            )





            if report and len(report) > 30:

                final_answer = report


            elif factcheck and len(factcheck) > 30:

                final_answer = factcheck


            elif summary and len(summary) > 30:

                final_answer = summary


            else:

                final_answer = research_notes





            final_answer = final_answer.strip()





            if len(final_answer) < 10:


                final_answer = (

                    "I don't have enough reliable "

                    "information to answer this."

                )






            import re

            tokens = re.split(r'(\s+)', final_answer)


            for token in tokens:

                if token:

                    yield token

                    time.sleep(0.005)







        except Exception as e:



            print(

                "Research Error:",

                e

            )




            final_answer = (

                "I don't have enough reliable "

                "information to answer this."

            )



            yield final_answer






        save_message(

            session_id,

            "assistant",

            final_answer

        )






    return StreamingResponse(

        generate(),

        media_type="text/plain",

        headers={

            "X-Session-Id": session_id

        }

    )