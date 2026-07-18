import os
from flask import Flask, render_template, request, jsonify, make_response
from src.crew import create_crew
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = (data.get("topic", "") if data else "").strip()

    if not topic:
        return jsonify({"error": "Topic cannot be empty."}), 400

    try:
        crew = create_crew(topic)
        result = crew.kickoff()
        return jsonify({"topic": topic, "blog": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    data = request.get_json()
    topic = (data.get("topic", "Blog") if data else "Blog").strip()
    blog = (data.get("blog", "") if data else "").strip()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, spaceAfter=16)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=18, spaceAfter=8)

    story = [Paragraph(topic, title_style), Spacer(1, 0.4*cm)]
    for line in blog.split("\n"):
        line = line.strip()
        if line:
            story.append(Paragraph(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), body_style))
        else:
            story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{topic[:40]}.pdf"'
    return response


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)