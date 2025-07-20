import os
import glob
import streamlit as st
from datetime import datetime
import time
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableSequence,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from MultiDocRAG.parse import parse_file,get_newly_parsed_basenames
from MultiDocRAG.retriever import initialize_retriever,format_docs,get_history_file,chunk_newly_parsed_grouped
from MultiDocRAG.prompts import system_prompt


load_dotenv()
api_key = os.getenv("api_key")

UPLOAD_FOLDER = "uploaded_documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="Multiple Documents QA System",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("📄 Multiple Documents Question Answer System")

# --- Initialize session state keys ---
if "docs_uploaded" not in st.session_state:
    st.session_state.docs_uploaded = False
if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []
if "newly_parsed" not in st.session_state:
    st.session_state.newly_parsed = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "grouped_chunks" not in st.session_state:
    st.session_state.grouped_chunks = {}
if "selected_chunks" not in st.session_state:
    st.session_state.selected_chunks = {}

# --- Sidebar ---
with st.sidebar.container(border=True):
    st.sidebar.subheader("📤 Upload Your Documents")

    if st.session_state.docs_uploaded:
        st.success("✅ Files uploaded successfully:")
        for name in st.session_state.uploaded_file_names:
            st.markdown(f"• {name}")

        if st.sidebar.button("🔄 Upload Again"):
            # Clear all relevant states for fresh upload
            st.session_state.docs_uploaded = False
            st.session_state.uploaded_file_names = []
            st.session_state.newly_parsed = []
            st.session_state.retriever = None
            st.session_state.chat_history = []
            st.rerun()

    else:
        uploaded_files = st.sidebar.file_uploader(
            "Select files",
            accept_multiple_files=True,
            key="file_uploader"
        )
        if uploaded_files:
            with st.spinner(f"Uploading and processing {len(uploaded_files)} file(s)..."):
                time.sleep(2)  # simulate delay

                uploaded_names = []
                for file in uploaded_files:
                    file_path = os.path.join(UPLOAD_FOLDER, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    uploaded_names.append(file.name)

                # Update session state and rerun
                st.session_state.uploaded_file_names = uploaded_names
                st.session_state.docs_uploaded = True
                st.rerun()
                

# --- Main area ---
if not st.session_state.docs_uploaded:
    st.info("Please upload documents via the sidebar to start the chat.")
else:
    # Parse files once
    if not st.session_state.newly_parsed:
          # ensure this writes parsed data somewhere
        st.session_state.newly_parsed = get_newly_parsed_basenames()
        parse_file()
        
    if st.session_state.newly_parsed:
        new_chunks = chunk_newly_parsed_grouped(st.session_state.newly_parsed)
        st.session_state.grouped_chunks.update(new_chunks)

    # Initialize retriever once
    if st.session_state.retriever is None:
        try:
            st.session_state.retriever = initialize_retriever(api_key, st.session_state.newly_parsed)
        except Exception as e:
            st.error(f"Error initializing retriever: {str(e)}")
            st.stop()

    retriever = st.session_state.retriever
    
    view_mode = st.sidebar.selectbox(
      "🔎 View",
      ["Chat", "View Chunks", "View Parsed Files"]
    )

    

    def get_parsed_files(output_dir="output"):
        # Finds all *.md files recursively inside output directory
        return glob.glob(os.path.join(output_dir, "**/*.md"), recursive=True)

    def read_parsed_file(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

  
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        MessagesPlaceholder(variable_name='history'),
        HumanMessagePromptTemplate.from_template("""
			Context:
			{context}

			Question:
			{question}
		""")
    ])
    
    llm = ChatMistralAI(
        model="mistral-small",
        temperature=0.2,
        api_key=api_key
    )
  

    def chat_with_model(question,session_id= "default"):
        retrieval_chain = RunnableSequence(
        {
            "context": RunnableLambda(lambda x: x["question"]) | retriever | RunnableLambda(format_docs),
            "question": RunnableLambda(lambda x: x["question"]),
            "history": RunnableLambda(lambda x: x.get("history", [])),  
        }
        | prompt
        | llm
        | StrOutputParser())
        
        retrieval_chain_with_memory = RunnableWithMessageHistory(
        runnable=retrieval_chain,
        get_message_history=get_history_file,
        get_session_history=get_history_file, 
        input_messages_key="question",
        history_messages_key="history")
        
        result = retrieval_chain_with_memory.invoke(
            {"question": question},
            config={"configurable": {"session_id": session_id}},
        )
        return result
    
    
    if view_mode == "View Chunks":
      st.header("🧩 View Parsed Chunks")

      if "grouped_chunks" in st.session_state and st.session_state.grouped_chunks:
          file_to_view = st.selectbox("📄 Select a file", list(st.session_state.grouped_chunks.keys()))
          selected_chunks = st.session_state.grouped_chunks[file_to_view]

          st.markdown(f"**Total Chunks:** {len(selected_chunks)}")
          show_all = st.checkbox("Show all chunks")

          if show_all:
              st.subheader(f"📄 All Chunks from {file_to_view}")
              for doc in selected_chunks:
                  st.markdown(f"**Chunk {doc.metadata['chunk_id']}:**")
                  st.write(doc.page_content)
          else:
              chunk_labels = [f"Chunk {doc.metadata['chunk_id']}" for doc in selected_chunks]
              selected_label = st.selectbox("Select a chunk to view", chunk_labels)
              selected_index = int(selected_label.split()[-1])
              doc = selected_chunks[selected_index]

              st.subheader(f"📄 Chunk {doc.metadata['chunk_id']}")
              st.write(doc.page_content)
      else:
          st.info("No parsed chunks found. Upload and parse documents first.")

    elif view_mode == "View Parsed Files":
        st.header("📄 View Parsed Files")

        newly_parsed = st.session_state.get("newly_parsed", [])
        if not newly_parsed:
            st.info("No newly parsed files available.")
        else:
            parsed_files = []
            for base in newly_parsed:
                md_path = os.path.join("output", base, f"{base}.md")
                if os.path.isfile(md_path):
                    parsed_files.append(md_path)

            if not parsed_files:
                st.info("No parsed .md files found for the newly parsed documents.")
            else:
                display_files = [os.path.relpath(f, "output") for f in parsed_files]
                selected_file = st.selectbox("Select a parsed file", display_files)
                full_path = os.path.join("output", selected_file)

                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                st.markdown(f"### {selected_file}")
                st.text_area("File Content", content, height=600)

      

    elif view_mode == "Chat":
      st.header("💬 Chat with your documents")

      if st.button("🔄 New Chat"):
          st.session_state.chat_history = []
          st.rerun()

      for chat in st.session_state.chat_history:
          with st.chat_message("user"):
              st.markdown(chat["user"])
              st.caption(chat["user_time"])

          with st.chat_message("assistant"):
              st.markdown(chat["bot"])
              st.caption(chat["bot_time"])

      if user_input := st.chat_input("Ask anything..."):
          user_time = datetime.now().strftime("%I:%M %p")

          with st.chat_message("user"):
              st.markdown(user_input)
              st.caption(user_time)

          with st.spinner("Thinking..."):
              bot_response = chat_with_model(user_input)
              bot_time = datetime.now().strftime("%I:%M %p")

          with st.chat_message("assistant"):
              st.markdown(bot_response)
              st.caption(bot_time)

          st.session_state.chat_history.append({
              "user": user_input,
              "bot": bot_response,
              "user_time": user_time,
              "bot_time": bot_time
          })
