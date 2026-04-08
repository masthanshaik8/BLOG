from flask import Flask, render_template, request
from src.crew import create_crew

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic = request.form["topic"]

        # Run CrewAI
        crew = create_crew(topic)
        result = crew.kickoff()

        return render_template("result.html", topic=topic, blog=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)