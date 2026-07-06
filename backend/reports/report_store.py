import os


REPORT_DIR = "reports_store"


os.makedirs(

    REPORT_DIR,

    exist_ok=True

)


def save_report(

    report_id,

    content

):

    path = os.path.join(

        REPORT_DIR,

        f"{report_id}.md"

    )


    with open(

        path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(content)


def load_report(

    report_id

):

    path = os.path.join(

        REPORT_DIR,

        f"{report_id}.md"

    )


    if os.path.exists(path):

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            return f.read()


    return None