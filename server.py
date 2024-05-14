from rag import ChatPDF
import streamlit as st
from langchain_community.chat_models import ChatOllama
import tempfile
import os
from  prompt import *

st.session_state["nb_files"] = 0
st.session_state["model"] = ChatPDF()
st.session_state["model2"] = ChatOllama()
st.session_state["path"] = ""

def file_handler():
  paths = set()
  for file in st.session_state["file_uploader"]:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, file.name)
    with open(path, 'wb') as f:
      f.write(file.getvalue())
    paths.add(path)
  return paths 


st.title("EduCopilot")

genre = st.sidebar.radio(
  "set mode 👇",
  ["field specific", "general purpose"]
)

#st.sidebar.subheader("Choose Files As Context (RAG)")

files = st.sidebar.file_uploader(
  "Upload documents",
  type=["pdf"],
  key="file_uploader",
  label_visibility="collapsed",
  accept_multiple_files=True,
  on_change= file_handler
)



#st.sidebar.subheader("Parameters")
genre = st.sidebar.selectbox(
  "Select Answer Type (Prompt)",
  ("Definition", "story telling", "instructional scenario (latex)","translation","rectifying my scenario")
)


if "messages" not in st.session_state :
  st.session_state.messages = []

for message in st.session_state.messages :
  with st.chat_message(message["role"]) :
    st.write(message["content"])


#get user input and proccess it
if prompt := st.chat_input("what is up ?") :
  with st.chat_message("user"):
    st.markdown(prompt)
  
  st.session_state.messages.append({"role":"user","content":prompt})

  response = ""

  with st.chat_message("assistant"): 
    if len(files) :
      paths = file_handler()  # Call the function to get paths
      if genre == "story telling":
        st.session_state["model"].ingests(paths,f_string=story_telling())
      elif genre == "instructional scenario (latex)":
        st.session_state["model"].ingests(paths,f_string=instructional_scenario())
      else :
        st.session_state["model"].ingests(paths)
      response = st.write_stream(st.session_state["model"].chain.stream(prompt))
    else :
      print("no files found")
      response = st.write_stream(st.session_state["model2"].stream(prompt))

  st.session_state.messages.append({"role":"assistant","content": response})