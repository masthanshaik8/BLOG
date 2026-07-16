import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def clean(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    return text.strip()


def chat(system, user):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return clean(response.choices[0].message.content)


def create_crew(topic):
    return BlogPipeline(topic)


class BlogPipeline:
    def __init__(self, topic):
        self.topic = topic

    def kickoff(self):
        research = chat(
            "You are a Senior Research Analyst. Provide detailed, accurate insights on the given topic.",
            f"Research this topic thoroughly and provide key insights: {self.topic}",
        )

        draft = chat(
            "You are a Professional Blog Writer. Write engaging, well-structured blog posts based on research.",
            f"Write a complete blog article about '{self.topic}' using this research:\n\n{research}",
        )

        final = chat(
            "You are a Content Editor. Polish blog posts for grammar, clarity, flow, and quality.",
            f"Edit and improve this blog article:\n\n{draft}",
        )

        self._save_outputs(research, draft, final)
        return final

    def _save_outputs(self, research, draft, final):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out = os.path.join(base, "outputs")
        os.makedirs(out, exist_ok=True)
        for name, content in [("research_output.md", research), ("draft_blog.md", draft), ("final_blog.md", final)]:
            with open(os.path.join(out, name), "w", encoding="utf-8") as f:
                f.write(content)
