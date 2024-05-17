from dotenv import load_dotenv
import os
import streamlit as st
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
import warnings
from typing import Dict, Any

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


def create_task(
    description: str, expected_output: str, agent: Agent, tools: list = None
) -> Task:
    """
    Creates a task with the given parameters.

    Args:
        - description: The description of the task.
        - expected_output: The expected output of the task.
        - agent: The agent responsible for the task.
        - tools: A list of tools to be used by the agent.

    Returns:
        - An instance of the Task class.
    """
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        tools=tools or [],
    )


def create_crew(agents: list, tasks: list, verbose: int, memory: bool) -> Crew:
    """
    Creates a crew with the given agents and tasks.

    Args:
        - agents: A list of Agent instances.
        - tasks: A list of Task instances.
        - verbose: The verbosity level.
        - memory: Whether the crew should use memory.

    Returns:
        - An instance of the Crew class.
    """
    return Crew(agents=agents, tasks=tasks, verbose=verbose, memory=memory)


def initialize_agents() -> Dict[str, Agent]:
    """
    Initializes the support agent and support quality assurance agent.

    Returns:
        - A dictionary with initialized agents.
    """
    support_agent = create_agent(
        role="Senior Support Representative",
        goal="Be the most friendly and helpful support representative in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and are now working on providing "
            "support to {customer}, a super important customer for your company. "
            "You need to make sure that you provide the best support! "
            "Make sure to provide full complete answers, and make no assumptions."
        ),
        allow_delegation=False,
        verbose=True,
    )

    support_quality_assurance_agent = create_agent(
        role="Support Quality Assurance Specialist",
        goal="Get recognition for providing the best support quality assurance in your team",
        backstory=(
            "You work at crewAI (https://crewai.com) and are now working with your team "
            "on a request from {customer} ensuring that the support representative is "
            "providing the best support possible. "
            "You need to make sure that the support representative is providing full "
            "complete answers, and make no assumptions."
        ),
        allow_delegation=True,
        verbose=True,
    )

    return {
        "support_agent": support_agent,
        "support_quality_assurance_agent": support_quality_assurance_agent,
    }


def initialize_tasks(agents: Dict[str, Agent]) -> list:
    """
    Initializes the tasks for the support agent and support quality assurance agent.

    Args:
        - agents: A dictionary with initialized agents.

    Returns:
        - A list of Task instances.
    """
    docs_scrape_tool = ScrapeWebsiteTool(
        website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
    )

    inquiry_resolution = create_task(
        description=(
            "{customer} just reached out with a super important ask:\n"
            "{inquiry}\n\n"
            "{person} from {customer} is the one that reached out. "
            "Make sure to use everything you know to provide the best support possible. "
            "You must strive to provide a complete and accurate response to the customer's inquiry."
        ),
        expected_output=(
            "A detailed, informative response to the customer's inquiry that addresses "
            "all aspects of their question. The response should include references "
            "to everything you used to find the answer, including external data or solutions. "
            "Ensure the answer is complete, leaving no questions unanswered, and maintain a helpful and friendly tone throughout."
        ),
        agent=agents["support_agent"],
        tools=[docs_scrape_tool],
    )

    quality_assurance_review = create_task(
        description=(
            "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
            "Ensure that the answer is comprehensive, accurate, and adheres to the high-quality standards expected for customer support. "
            "Verify that all parts of the customer's inquiry have been addressed thoroughly, with a helpful and friendly tone. "
            "Check for references and sources used to find the information, ensuring the response is well-supported and leaves no questions unanswered."
        ),
        expected_output=(
            "A final, detailed, and informative response ready to be sent to the customer. "
            "This response should fully address the customer's inquiry, incorporating all relevant feedback and improvements. "
            "Don't be too formal, we are a chill and cool company but maintain a professional and friendly tone throughout."
        ),
        agent=agents["support_quality_assurance_agent"],
    )

    return [inquiry_resolution, quality_assurance_review]


def run_crew(inputs: Dict[str, Any], verbose: int, memory: bool) -> str:
    """
    Runs the multi-agent system to generate a support response based on the given inputs.

    Args:
        - inputs: The input parameters for the task.
        - verbose: The verbosity level.
        - memory: Whether the crew should use memory.

    Returns:
        - The generated response in markdown format.
    """
    agents = initialize_agents()
    tasks = initialize_tasks(agents)
    crew = create_crew(
        agents=[agents["support_agent"], agents["support_quality_assurance_agent"]],
        tasks=tasks,
        verbose=verbose,
        memory=memory,
    )
    result = crew.kickoff(inputs=inputs)
    return result


def main():
    """
    Main function to run the Streamlit UI.
    """
    st.title("Customer Support Response Generator")

    customer = st.text_input("Enter the customer's name:", value="DeepLearningAI")
    person = st.text_input("Enter the contact person's name:", value="Andrew Ng")
    inquiry = st.text_area(
        "Enter the customer's inquiry:",
        value="I need help with setting up a Crew and kicking it off, specifically how can I add memory to my crew? Can you provide guidance?",
    )
    verbose = st.selectbox("Select verbosity level:", [0, 1, 2], index=2)
    memory = st.checkbox("Enable memory for the crew", value=True)

    if st.button("Generate Response"):
        inputs = {"customer": customer, "person": person, "inquiry": inquiry}
        result = run_crew(inputs, verbose, memory)
        st.markdown("### Generated Response")
        st.markdown(result)


if __name__ == "__main__":
    main()
