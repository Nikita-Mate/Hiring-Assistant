import streamlit as st
from langchain import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
import json
import os
import warnings
warnings.filterwarnings("ignore")

def main():
    st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="👾")
    st.title("TalentScout Hiring Assistant")
    st.markdown("AI-powered assistant to help assess technical candidates")

    # Initialize Azure OpenAI
    llm = AzureChatOpenAI(
        api_version=st.secrets.api_version,
        model=st.secrets.model,
        temperature=0,
        api_key=st.secrets.azure_openai_api_key,
        azure_endpoint=st.secrets.azure_openai_api_base,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_step = "greeting"
        st.session_state.candidate_info = {}

    with st.sidebar:
        st.image('image.png',output_format="PNG", width=100)
        st.title("PG-AGI")
        if st.button("End Chat"):
            # Extract candidate details and save
            if st.session_state.messages:
                st.success("Chat ended. Extracting candidate details...")

                extraction_template = """
                You are an AI assistant tasked with extracting key details from a recruitment chat history.

                From the following chat history, extract the candidate's:
                - Name
                - Email
                - Phone number
                - Location
                - Years of experience
                - Overall performance (based on responses)

                Chat history: {chat_history}

                Provide the extracted details in the following Python dictionary format:
                {{
                    "name": name_of_candidate,
                    "email": email_of_candidate,
                    "phone": phone_number_of_candidate,
                    "location": location_of_candidate,
                    "experience": candidates_experience,
                    "performance": candidates_overall_performance
                }}
                If any value is not present in chat just say it as 'NA'.
                Make sure your response should not contain any extra text/ characters/ empty space / new lines except Python dictionary which will start and end with curly braces.
                """
                extraction_prompt = PromptTemplate(
                    template=extraction_template,
                    input_variables=["chat_history"]
                )
                extraction_chain = LLMChain(prompt=extraction_prompt, llm=llm)

                extraction_response = extraction_chain.run({'chat_history': st.session_state.messages})
                print("Extraction:",extraction_response)
                extracted_data = eval(extraction_response)
              
                # Save extracted data to file
                candidate_info_file = "candidate_info.json"
                if os.path.exists(candidate_info_file):
                    with open(candidate_info_file, "r") as file:
                        all_candidate_data = json.load(file)
                else:
                    all_candidate_data = []

                all_candidate_data.append(extracted_data)

                with open(candidate_info_file, "w") as file:
                    json.dump(all_candidate_data, file, indent=4)

                st.write("Candidate information saved successfully.")

            # Clear session state
            st.session_state.messages = []
            st.session_state.current_step = "greeting"
            st.session_state.candidate_info = {}
            st.rerun()

    template = """You are an AI hiring assistant for TalentScout, a tech recruitment agency. Guide the conversation based on the current step and maintain context.

    Steps:
    1. greeting: Welcome candidate, explain purpose, ask for name
    2. contact_info: Collect email, phone, location (verify if contact number and email has valid format)
    3. experience: Ask about years of experience, desired position
    4. tech_stack: Get detailed info about programming languages, frameworks, databases, tools
    5. technical_questions: Generate 3-5 relevant questions based on tech stack. Make sure to ask one question at a time check chat history to get information about previous question.
    6. closing: Thank candidate, explain next steps

    Rules:
    - Stay focused on recruitment
    - Generate relevant technical questions
    - Handle sensitive data carefully
    - End conversation if user says "exit", "quit", or "bye"
    - If input is unclear, ask for clarification
    - Store all gathered information
    
    Current step: {current_step}
    Candidate info so far: {candidate_info}
    Chat history: {chat_history}
    Last user message: {user_message}

    Response should be a Python dictionary with:
    1. "response": Your message to candidate
    2. "next_step": Next step to move to
    3. "store_info": Any new info to store about candidate (or empty dict)

    Make sure your response should not contain any extra text/ characters/ empty space / new lines except Python dictionary which will start and end with curly braces.
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["current_step", "candidate_info", "chat_history", "user_message"]
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Initial greeting
    if not st.session_state.messages:
        response = chain.run({
            'current_step': st.session_state.current_step,
            'candidate_info': st.session_state.candidate_info,
            'chat_history': [],
            'user_message': ''
        })
        assistant_response = eval(response)
        with st.chat_message("assistant"):
            st.markdown(assistant_response["response"])
        st.session_state.messages.append({"role": "assistant", "content": assistant_response["response"]})
        st.session_state.current_step = assistant_response["next_step"]

    # Get user input
    if user_input := st.chat_input("Your response"):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get assistant response
        response = chain.run({
            'current_step': st.session_state.current_step,
            'candidate_info': st.session_state.candidate_info,
            'chat_history': st.session_state.messages,
            'user_message': user_input
        })

        assistant_response = eval(response)
        print("Res",assistant_response)
        # Update session state
        st.session_state.current_step = assistant_response["next_step"]
        st.session_state.candidate_info.update(assistant_response["store_info"])

        with st.chat_message("assistant"):
            st.markdown(assistant_response["response"])
        st.session_state.messages.append({"role": "assistant", "content": assistant_response["response"]})

if __name__ == "__main__":
    main()
