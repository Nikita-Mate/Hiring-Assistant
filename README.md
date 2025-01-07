# TalentScout Hiring Assistant 👾

TalentScout Hiring Assistant is an AI-powered chatbot designed to assist with assessing technical candidates during recruitment. This Streamlit-based application leverages Azure OpenAI for natural language processing to guide structured interviews and extract candidate details seamlessly.

## Features
- Welcomes candidates and explains the purpose of the interview.
- Collects candidate contact information (name, email, phone, location).
- Asks about the candidate's experience and desired position.
- Gathers details about the candidate's technical skills (programming languages, frameworks, tools, etc.).
- Generates and asks 3-5 technical questions based on the candidate's tech stack.
- Extracts key candidate information from the chat history and saves it to a JSON file.

## Tech Stack
- **Streamlit**: Web application framework.
- **Azure OpenAI**: LLM for natural language processing.
- **LangChain**: Framework for managing LLM prompts and responses.
- **Python**: Programming language.

## Installation

### Prerequisites
- Python 3.11
- Azure OpenAI API credentials
- Streamlit installed

### Steps
1. Clone the repository:
   bash
   git clone https://github.com/Nikita-Mate/Hiring-Assistant.git
   cd Hiring-Assistant
2. Install the dependencies:
  bash
  pip install -r requirements.txt
3. Create a secrets.toml file in the .streamlit folder and add your Azure OpenAI credentials:
  toml
  [default]
  azure_openai_api_key = "your_api_key"
  azure_openai_api_base = "your_azure_endpoint"
  api_version = "your_api_version"
  model = "your_model_name"
4. Run the application:
  bash
  streamlit run app.py
