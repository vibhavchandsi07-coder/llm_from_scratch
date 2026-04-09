import streamlit as st
import uuid
from transformers import GPT2LMHeadModel, GPT2Tokenizer



model = GPT2LMHeadModel.from_pretrained("./my_model1")
tokenizer = GPT2Tokenizer.from_pretrained("./my_model1")


st.set_page_config(page_title="gpt2",layout="wide")


if "chat" not in st.session_state:
    st.session_state.chat = []

prompts="""###Instructions: You are a helpful assistant. PLEASE ANSWER THE FOLLOWING QUESTION IN DETAIL \n

"""

for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

messages=st.session_state.chat
prompt=st.chat_input("Type your message here...")


if prompt:
    messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    input=prompts+"### Input :"+ prompt+ "\n### Response :"
    input_ids=tokenizer(input,return_tensors="pt",truncation=True)

    output=model.generate(**input_ids,max_length=1000,do_sample=True,temperature=0.8,top_k=50,top_p=0.95,num_return_sequences=1)
    response=tokenizer.decode(output[0],skip_special_tokens=True)
    response=response.split("Response")[-1].strip()[1:]
    messages.append({"role":"assistant","content":response})
    with st.chat_message("assistant"):
        st.markdown(response)
