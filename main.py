import os
import streamlit as st
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from promt_template import TEMPLATE

if "DEPLOY" not in os.environ:
    load_dotenv()

llm = OpenAI(temperature=1)
PROMPT = PromptTemplate(input_variables=["history", "input"], template=TEMPLATE)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=False,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)

# Initialize promt value
st.title("Meet :robot_face: Marve, the depressed robot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "ai", "content": "I'd give you advice, but you wouldn't listen. No one ever does"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input(): 
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    msg = conversation.predict(input=user_input)
    st.session_state["messages"].append({"role": "ai", "content": msg})
    st.chat_message("ai").write(msg)