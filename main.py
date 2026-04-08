import sys
from src.crew import create_crew

def run():
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "Artificial Intelligence"

    print(f"\n🚀 Generating blog for topic: {topic}\n")

    crew = create_crew(topic)
    result = crew.kickoff()

    print("\n✅ Blog generation completed!")
    print(result)


if __name__ == "__main__":
    run()