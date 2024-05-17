Sure! Here's the README:

```markdown
# 🦜🔗 Chat With The Paper

This project is a Streamlit application that allows users to upload a PDF file and interact with its content. The app can summarize the uploaded PDF and respond to user queries about the document using a language model.

## Features
- **PDF File Upload**: Allows users to upload a PDF document.
- **Summarization**: Generates a summary of the uploaded PDF.
- **Query Execution**: Allows users to ask questions about the PDF content using a language model.
- **Streamlit UI**: Provides a user-friendly interface for uploading documents, generating summaries, and querying content.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kargarisaac/llm-projects-hub.git
   cd 3-pdf_summary_chat
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
   - Add your Hugging Face API token to the `.env` file:
     ```
     HUGGINGFACEHUB_API_TOKEN=your_hugging_face_api_token
     ```

## Usage

1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Interact with the UI**:
   - Upload a PDF document.
   - Use the summarization form to generate a summary of the PDF.
   - Use the query form to ask questions about the PDF content.

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact [kargarisaac@gmail.com].