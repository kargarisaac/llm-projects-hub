from dotenv import load_dotenv
import os
import streamlit as st
from crewai import Agent, Task, Crew
import warnings
from typing import Dict

# Load environment variables from .env file
load_dotenv()

# Disable warnings
warnings.filterwarnings("ignore")

# Set OpenAI API key and model name from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"


def create_agent(
    role: str, goal: str, backstory: str, allow_delegation: bool, verbose: bool
) -> Agent:
    """
    Creates an agent with the given parameters.

    Args:
        - role: The role of the agent.
        - goal: The goal of the agent.
        - backstory: The backstory of the agent.
        - allow_delegation: Whether the agent can delegate tasks.
        - verbose: Whether the agent should operate in verbose mode.

    Returns:
        - An instance of the Agent class.
    """
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        allow_delegation=allow_delegation,
        verbose=verbose,
    )


def create_task(description: str, expected_output: str, agent: Agent) -> Task:
    """
    Creates a task with the given parameters.

    Args:
        - description: The description of the task.
        - expected_output: The expected output of the task.
        - agent: The agent responsible for the task.

    Returns:
        - An instance of the Task class.
    """
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )


def create_crew(agents: list, tasks: list, verbose: int) -> Crew:
    """
    Creates a crew with the given agents and tasks.

    Args:
        - agents: A list of Agent instances.
        - tasks: A list of Task instances.
        - verbose: The verbosity level.

    Returns:
        - An instance of the Crew class.
    """
    return Crew(agents=agents, tasks=tasks, verbose=verbose)


def initialize_agents() -> Dict[str, Agent]:
    """
    Initializes the content planner, writer, and editor agents.

    Returns:
        - A dictionary with initialized agents.
    """
    planner = create_agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article about the topic: {topic}. You collect information that helps the audience learn something and make informed decisions. Your work is the basis for the Content Writer to write an article on this topic.",
        allow_delegation=False,
        verbose=True,
    )

    writer = create_agent(
        role="Content Writer",
        goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
        backstory="You're working on a writing a new opinion piece about the topic: {topic}. You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic. You follow the main objectives and direction of the outline, as provided by the Content Planner. You also provide objective and impartial insights and back them up with information provided by the Content Planner. You acknowledge in your opinion piece when your statements are opinions as opposed to objective statements.",
        allow_delegation=False,
        verbose=True,
    )

    editor = create_agent(
        role="Editor",
        goal="Edit a given blog post to align with the writing style of the organization.",
        backstory="You are an editor who receives a blog post from the Content Writer. Your goal is to review the blog post to ensure that it follows journalistic best practices, provides balanced viewpoints when providing opinions or assertions, and also avoids major controversial topics or opinions when possible.",
        allow_delegation=False,
        verbose=True,
    )

    return {"planner": planner, "writer": writer, "editor": editor}


def initialize_tasks(agents: Dict[str, Agent]) -> list:
    """
    Initializes the tasks for the content planner, writer, and editor.

    Args:
        - agents: A dictionary with initialized agents.

    Returns:
        - A list of Task instances.
    """
    plan = create_task(
        description=(
            "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering their interests and pain points.\n"
            "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
        agent=agents["planner"],
    )

    write = create_task(
        description=(
            "1. Use the content plan to craft a compelling blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/Subtitles are properly named in an engaging manner.\n"
            "4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        agent=agents["writer"],
    )

    edit = create_task(
        description=(
            "Proofread the given blog post for grammatical errors and alignment with the brand's voice."
        ),
        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        agent=agents["editor"],
    )

    return [plan, write, edit]


def run_crew(topic: str, verbose: int) -> str:
    """
    Runs the multi-agent system to generate content on the given topic.

    Args:
        - topic: The topic for the content.
        - verbose: The verbosity level.

    Returns:
        - The generated content in markdown format.
    """
    agents = initialize_agents()
    tasks = initialize_tasks(agents)
    crew = create_crew(
        agents=[agents["planner"], agents["writer"], agents["editor"]],
        tasks=tasks,
        verbose=verbose,
    )
    result = crew.kickoff(inputs={"topic": topic})
    return result


def main():
    """
    Main function to run the Streamlit UI.
    """
    st.title("Multi-Agent System Content Generator")

    topic = st.text_input(
        "Enter the topic for the content:", value="Artificial Intelligence"
    )
    verbose = st.selectbox("Select verbosity level:", [0, 1, 2], index=2)

    if st.button("Generate Content"):
        result = run_crew(topic, verbose)
        st.markdown("### Generated Content")
        st.markdown(result)


if __name__ == "__main__":
    main()
