# Customer Support Response Generator

This project uses a multi-agent system to generate a support response based on a given customer inquiry. The system consists of two agents: a Senior Support Representative and a Support Quality Assurance Specialist. Each agent performs a specific task to collaboratively produce a comprehensive and helpful support response. The project also includes a Streamlit UI for user interaction.

## Features
- **Multi-Agent System**: Utilizes two agents with distinct roles to generate and review support responses.
- **Streamlit UI**: Allows users to input customer details, inquiry, verbosity level, and memory option, and view the generated response.
- **Customizable Verbosity**: Users can select the level of detail for the logs.
- **Memory Option**: Users can enable or disable memory for the crew.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kargarisaac/llm-projects-hub.git
   cd 5-multi_agent_customer_support_automation
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
   - Enter the customer's name.
   - Enter the contact person's name.
   - Enter the customer's inquiry.
   - Select the verbosity level.
   - Enable or disable memory for the crew.
   - Click on "Generate Response" to see the results.

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact [kargarisaac@gmail.com].
