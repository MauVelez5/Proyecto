import streamlit as st

st.title("Lectura Inteligente")
import os
#from dotenv import load_dotenv
import streamlit as st
import time
import glob
from gtts import gTTS
from PIL import Image
import PyPDF2
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

st.markdown("<h1 style='color: white;'>PDF Assistant</h1>", unsafe_allow_html=True) 
st.markdown("<h3 style='color: white; font-size: 18px;'> Bienvenido estudiante EAFITENSE, este es un espacio de aprendizaje en el cual podrás encontrar información clave dentro de tus Pdf's muy fácil y rápido. ¡Explórala!</h3>", unsafe_allow_html=True)
st.markdown("<h2 style='color: white;'>Chatea con tu PDF 💬</h2>", unsafe_allow_html=True) 
image = Image.open('asistente_pdf.jpg')
st.image (image, width=500)
st.markdown("""<style>.stApp {background-color: #4e93fa;  /* Cambia este valor al color de fondo que desees */}</style>""",unsafe_allow_html=True)
ke = st.text_input('Ingresa tu Clave')
#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['OPENAI_API_KEY'] = ke

pdfFileObj = open('example.pdf', 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)


    # upload file
pdf = st.file_uploader("Carga el archivo PDF", type="pdf")

   # extract the text
if pdf is not None:
      from langchain.text_splitter import CharacterTextSplitter
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
         text += page.extract_text()

   # split into chunks
      text_splitter = CharacterTextSplitter(separator="\n",chunk_size=500,chunk_overlap=20,length_function=len)
      chunks = text_splitter.split_text(text)

# create embeddings
      embeddings = OpenAIEmbeddings()
      knowledge_base = FAISS.from_texts(chunks, embeddings)

# show user input
      st.subheader("Escribe que quieres saber sobre el documento")
      user_question = st.text_input(" ")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)

        llm = OpenAI(model_name="gpt-4o")
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          print(cb)
        st.write(response)
try:
    os.mkdir("temp")
except:
    pass
 
# text_2 = st.text_input("Ingrese el texto.")

tld="es"

def text_to_speech(text, tld):
    
    tts = gTTS(response,"es", tld, slow=False)
    try:
        nombre_archivo = response[0:20]
    except:
        nombre_archivo = "audio"
    tts.save(f"temp/{nombre_archivo}.mp3")
    return nombre_archivo, response


#display_output_text = st.checkbox("Verifica el texto")

if st.button("Respuesta en Voz"):
    result, output_text = text_to_speech(response, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)



def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
