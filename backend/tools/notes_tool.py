import os



NOTES_DIR = "notes"


os.makedirs(

    NOTES_DIR,

    exist_ok=True

)


def save_notes(

    filename,

    content

):

    path = os.path.join(

        NOTES_DIR,

        filename

    )


    with open(

        path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(

            content

        )


def read_notes(

    filename

):

    path = os.path.join(

        NOTES_DIR,

        filename

    )


    if os.path.exists(path):

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            return f.read()


    return ""