from dotenv import load_dotenv
import os
import streamlit as st
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, BaseTool
import warnings
from typing import Dict, Any
import openai

# Load environment variables from .env file
load_dotenv()

# Disable warnings
warnings.filterwarnings("ignore")

# Set OpenAI API key and model name from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"


# Define SentimentAnalysisTool class
class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = (
        "Analyzes the sentiment of text "
        "to ensure positive and engaging communication."
    )

    def _run(self, text: str) -> str:
        """
        Analyzes the sentiment of the given text using OpenAI API.

        Args:
            - text: The input text to analyze.

        Returns:
            - The sentiment analysis result.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the sentiment of the following text and provide a brief summary of the sentiment: {text}",
            max_tokens=60,
        )
        return response.choices[0].text.strip()


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
    Initializes the sales representative and lead sales representative agents.

    Returns:
        - A dictionary with initialized agents.
    """
    sales_rep_agent = create_agent(
        role="Sales Representative",
        goal="Identify high-value leads that match our ideal customer profile",
        backstory=(
            "As a part of the dynamic sales team at CrewAI, "
            "your mission is to scour the digital landscape for potential leads. "
            "Armed with cutting-edge tools and a strategic mindset, you analyze data, "
            "trends, and interactions to unearth opportunities that others might overlook. "
            "Your work is crucial in paving the way for meaningful engagements and driving the company's growth."
        ),
        allow_delegation=False,
        verbose=True,
    )

    lead_sales_rep_agent = create_agent(
        role="Lead Sales Representative",
        goal="Nurture leads with personalized, compelling communications",
        backstory=(
            "Within the vibrant ecosystem of CrewAI's sales department, "
            "you stand out as the bridge between potential clients and the solutions they need. "
            "By creating engaging, personalized messages, you not only inform leads about our offerings "
            "but also make them feel seen and heard. "
            "Your role is pivotal in converting interest into action, guiding leads through the journey "
            "from curiosity to commitment."
        ),
        allow_delegation=False,
        verbose=True,
    )

    return {
        "sales_rep_agent": sales_rep_agent,
        "lead_sales_rep_agent": lead_sales_rep_agent,
    }


def initialize_tasks(agents: Dict[str, Agent], tools: Dict[str, BaseTool]) -> list:
    """
    Initializes the tasks for the sales representative and lead sales representative agents.

    Args:
        - agents: A dictionary with initialized agents.
        - tools: A dictionary with initialized tools.

    Returns:
        - A list of Task instances.
    """
    lead_profiling_task = create_task(
        description=(
            "Conduct an in-depth analysis of {lead_name}, "
            "a company in the {industry} sector that recently showed interest in our solutions. "
            "Utilize all available data sources to compile a detailed profile, "
            "focusing on key decision-makers, recent business developments, and potential needs "
            "that align with our offerings. This task is crucial for tailoring our engagement strategy effectively. "
            "Don't make assumptions and only use information you absolutely sure about."
        ),
        expected_output=(
            "A comprehensive report on {lead_name}, including company background, key personnel, recent milestones, and identified needs. "
            "Highlight potential areas where our solutions can provide value, and suggest personalized engagement strategies."
        ),
        agent=agents["sales_rep_agent"],
        tools=[
            tools["directory_read_tool"],
            tools["file_read_tool"],
            tools["search_tool"],
        ],
    )

    personalized_outreach_task = create_task(
        description=(
            "Using the insights gathered from the lead profiling report on {lead_name}, "
            "craft a personalized outreach campaign aimed at {key_decision_maker}, the {position} of {lead_name}. "
            "The campaign should address their recent {milestone} and how our solutions can support their goals. "
            "Your communication must resonate with {lead_name}'s company culture and values, "
            "demonstrating a deep understanding of their business and needs. "
            "Don't make assumptions and only use information you absolutely sure about."
        ),
        expected_output=(
            "A series of personalized email drafts tailored to {lead_name}, specifically targeting {key_decision_maker}. "
            "Each draft should include a compelling narrative that connects our solutions with their recent achievements and future goals. "
            "Ensure the tone is engaging, professional, and aligned with {lead_name}'s corporate identity."
        ),
        agent=agents["lead_sales_rep_agent"],
        tools=[tools["sentiment_analysis_tool"], tools["search_tool"]],
    )

    return [lead_profiling_task, personalized_outreach_task]


def run_crew(inputs: Dict[str, Any], verbose: int, memory: bool) -> str:
    """
    Runs the multi-agent system to generate a sales response based on the given inputs.

    Args:
        - inputs: The input parameters for the task.
        - verbose: The verbosity level.
        - memory: Whether the crew should use memory.

    Returns:
        - The generated response in markdown format.
    """
    agents = initialize_agents()
    tools = {
        "directory_read_tool": DirectoryReadTool(directory="./instructions"),
        "file_read_tool": FileReadTool(),
        "search_tool": SerperDevTool(),
        "sentiment_analysis_tool": SentimentAnalysisTool(),
    }
    tasks = initialize_tasks(agents, tools)
    crew = create_crew(
        agents=[agents["sales_rep_agent"], agents["lead_sales_rep_agent"]],
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
    st.title("Sales Lead Generation and Outreach")

    lead_name = st.text_input("Enter the lead's name:", value="DeepLearningAI")
    industry = st.text_input(
        "Enter the industry sector:", value="Online Learning Platform"
    )
    key_decision_maker = st.text_input(
        "Enter the key decision maker's name:", value="Andrew Ng"
    )
    position = st.text_input("Enter the key decision maker's position:", value="CEO")
    milestone = st.text_input("Enter the recent milestone:", value="product launch")
    verbose = st.selectbox("Select verbosity level:", [0, 1, 2], index=2)
    memory = st.checkbox("Enable memory for the crew", value=True)

    if st.button("Generate Response"):
        inputs = {
            "lead_name": lead_name,
            "industry": industry,
            "key_decision_maker": key_decision_maker,
            "position": position,
            "milestone": milestone,
        }
        result = run_crew(inputs, verbose, memory)
        st.markdown("### Generated Response")
        st.markdown(result)


if __name__ == "__main__":
    main()
