# 🦜🔗 Ask The Doc App

This project is a Streamlit application that allows users to upload a document and query the content using a language model. The app loads the document, splits it into chunks, and generates responses to user queries using a RetrievalQA chain.

## Features
- **Document Upload**: Allows users to upload a text document.
- **Query Execution**: Allows users to ask questions about the document content using a language model.
- **Streamlit UI**: Provides a user-friendly interface for uploading documents and querying content.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kargarisaac/llm-projects-hub.git
   cd 2-ask_doc
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
   - Upload a text document.
   - Enter your query about the document content.
   - Submit the form to see the generated response.

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact [kargarisaac@gmail.com].
