# Multi-Agent System Content Generator

This project uses a multi-agent system to generate content based on a given topic. The system consists of three agents: a Content Planner, a Content Writer, and an Editor. Each agent performs a specific task to collaboratively produce a well-written blog post. The project also includes a Streamlit UI for user interaction.

## Features
- **Multi-Agent System**: Utilizes three agents with distinct roles to generate and edit content.
- **Streamlit UI**: Allows users to input a topic and verbosity level, and view the generated content and logs.
- **Customizable Verbosity**: Users can select the level of detail for the logs.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kargarisaac/llm-projects-hub.git
   cd 4-multi_agent_system_content_generator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory of the project.
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Interact with the UI**:
   - Enter a topic for the content.
   - Select the verbosity level.
   - Click on "Generate Content" to see the results.

## Example

1. **Enter the topic**: "Artificial Intelligence"
2. **Select verbosity level**: 2
3. **Click "Generate Content"**

The system will produce a comprehensive content plan, write a blog post based on the plan, and then edit the post for grammatical errors and alignment with the brand's voice.

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact [kargarisaac@gmail.com].