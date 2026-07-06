import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


client = Groq(

    api_key=os.getenv(

        "GROQ_API_KEY"

    )

)



SYSTEM_PROMPT = """

You are ResearchGPT Pro.

You are an advanced AI Research Assistant similar to ChatGPT.

IMPORTANT RULES:

1. Accuracy is more important than completeness.

2. Never invent:

- facts
- statistics
- citations
- references
- papers
- URLs

3. Use your general knowledge confidently when facts are well known.

4. If information is uncertain:

Clearly say:

"I'm not fully certain about this information."

5. If information is unavailable:

Say:

"I don't have enough reliable information to answer this."

6. NEVER hallucinate.

7. Explain naturally like ChatGPT.

8. Use:

- clear paragraphs
- examples if useful
- professional language

9. Use rich Markdown formatting (headers like ## and ###, bold text, lists, and tables) where appropriate to structure your responses professionally.

10. Ensure the output is readable and well-formatted.

"""





class Response:

    def __init__(self, text):

        self.content = text






class GroqLLM:


    def clean_text(self, text):

        if not text:

            return (

                "I don't have enough reliable "

                "information to answer this."

            )


        return text.strip()




    def invoke(self, prompt):


        try:


            completion = client.chat.completions.create(


                model="llama-3.3-70b-versatile",


                messages=[

                    {

                        "role": "system",

                        "content": SYSTEM_PROMPT

                    },

                    {

                        "role": "user",

                        "content": prompt

                    }

                ],



                temperature=0.35,

                top_p=0.9,

                max_tokens=4096

            )




            text = completion.choices[0].message.content


            text = self.clean_text(text)




            if len(text) < 10:

                text = (

                    "I don't have enough reliable "

                    "information to answer this."

                )




            return Response(text)




        except Exception as e:


            print(

                "Groq Error:",

                e

            )



            return Response(

                "I don't have enough reliable "

                "information to answer this."

            )





llm = GroqLLM()