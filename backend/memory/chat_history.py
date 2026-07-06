import json
import uuid
from datetime import datetime

from memory.redis_memory import redis_client




def create_session(title):

    session_id = str(uuid.uuid4())


    data = {

        "id": session_id,

        "title": title,

        "messages": [],

        "pinned": False,

        "created_at": datetime.utcnow().isoformat(),

        "updated_at": datetime.utcnow().isoformat()

    }


    redis_client.set(

        f"session:{session_id}",

        json.dumps(data)

    )


    return session_id






def save_message(

    session_id,

    role,

    content,

    file_name=None

):


    if not content and not file_name:

        return



    if content:

        content = content.strip()

    else:

        content = ""




    raw = redis_client.get(

        f"session:{session_id}"

    )


    if not raw:

        return



    data = json.loads(raw)


    msg = {

        "role": role,

        "content": content

    }

    if file_name:

        msg["file_name"] = file_name


    data["messages"].append(msg)



    data["updated_at"] = (

        datetime.utcnow().isoformat()

    )




    redis_client.set(

        f"session:{session_id}",

        json.dumps(data)

    )








def get_session(

    session_id

):


    data = redis_client.get(

        f"session:{session_id}"

    )


    if data:

        return json.loads(data)


    return {}








def get_all_sessions():

    sessions = []



    keys = redis_client.keys(

        "session:*"

    )



    for key in keys:


        raw = redis_client.get(key)


        if not raw:

            continue



        data = json.loads(raw)



        sessions.append({

            "id": data["id"],

            "title": data["title"],

            "pinned": data.get("pinned", False),

            "updated_at":

            data.get(

                "updated_at",

                ""

            )

        })





    sessions.sort(

        key=lambda x:

        x["updated_at"],

        reverse=True

    )



    return sessions







def delete_session(

    session_id

):


    redis_client.delete(

        f"session:{session_id}"

    )








def rename_session(

    session_id,

    title

):


    data = get_session(

        session_id

    )



    if not data:

        return




    data["title"] = title



    data["updated_at"] = (

        datetime.utcnow().isoformat()

    )



    redis_client.set(

        f"session:{session_id}",

        json.dumps(data)

    )




def pin_session(

    session_id,

    pinned: bool

):

    data = get_session(session_id)

    if not data:

        return

    data["pinned"] = pinned

    redis_client.set(

        f"session:{session_id}",

        json.dumps(data)

    )