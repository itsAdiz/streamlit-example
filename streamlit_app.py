from openai import OpenAI
import streamlit as st
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer,header {visibility: hidden;}
          
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: ;'> 🥴 Doctur Adiz</h1>", unsafe_allow_html=True)


client = OpenAI(api_key=st.secrets["apikey"] , base_url=st.secrets["apiurl"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Send system message only once before starting the conversation
if not st.session_state.get("system_message_sent", False):
    st.session_state.messages.append({"role": "system", "content": st.secrets['ins']})
    st.session_state["system_message_sent"] = True

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Haan V... Ki haaal Aa tera"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[

                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
