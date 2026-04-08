from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import yaml
import os

load_dotenv()

# Load YAML configs
def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def create_crew(topic):
    agents_config = load_yaml("config/agents.yaml")
    tasks_config = load_yaml("config/tasks.yaml")

    # Agents
    researcher = Agent(
        role=agents_config["researcher"]["role"],
        goal=agents_config["researcher"]["goal"],
        backstory=agents_config["researcher"]["backstory"],
        verbose=True
    )

    writer = Agent(
        role=agents_config["writer"]["role"],
        goal=agents_config["writer"]["goal"],
        backstory=agents_config["writer"]["backstory"],
        verbose=True
    )

    editor = Agent(
        role=agents_config["editor"]["role"],
        goal=agents_config["editor"]["goal"],
        backstory=agents_config["editor"]["backstory"],
        verbose=True
    )

    # Tasks
    research_task = Task(
        description=tasks_config["research_task"]["description"].format(topic=topic),
        expected_output=tasks_config["research_task"]["expected_output"],
        agent=researcher,
        output_file="outputs/research_output.md"
    )

    writing_task = Task(
        description=tasks_config["writing_task"]["description"].format(topic=topic),
        expected_output=tasks_config["writing_task"]["expected_output"],
        agent=writer,
        output_file="outputs/draft_blog.md"
    )

    editing_task = Task(
        description=tasks_config["editing_task"]["description"].format(topic=topic),
        expected_output=tasks_config["editing_task"]["expected_output"],
        agent=editor,
        output_file="outputs/final_blog.md"
    )

    # Crew
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        verbose=True
    )

    return crew