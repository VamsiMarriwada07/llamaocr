import streamlit as st
from PIL import Image
import ollama

st.set_page_config(page_title="Image Chat",layout="centered")

st.title("Image Chat with llama3.2-Vision")
st.write("Upload an Image and ask questions about it.")

uploaded_file = st.file_uploader("Choose an image",type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_container_width=True)

    image_path = f"temp_{uploaded_file.name}"
    with open(image_path,"wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("The image has been uploaded, You can now ask questions about it. ")

    question = st.text_input("Ask a question about the image : ")
    if question:
        with st.spinner("Thinking...."):
            try:
                response = ollama.chat(
                    model="llama3.2-vision",
                    messages=[
                        {
                            'role':'user',
                            'content':question,
                            'images':[image_path]
                        }
                    ]
                )
                content = response["message"]["content"]
                st.success("Answer:")
                st.write(content)
            except Exception as e:
                st.error("An error occured while processing your question.")
                st.error(str(e))
    else:
        st.info("Please upload an image to get started.")