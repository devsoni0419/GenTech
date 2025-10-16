import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import google.generativeai as genai
# st.header('AI MATHEMATICS ASSISTANT')
html='''
<style>
header{
    [data-testside='stheader']{
        background-color:#000
        color:#FFF
    }
    [data-testside='stheader']::after{
        content:'AI MATHEMATICS ASSISTANT'
        text-align:center
    }
}
</style>
'''
st.html('<h1>AI MATHEMATICS ASSISTANT</h1>')
st.markdown(html,unsafe_allow_html=True)
st.title('Draw,Upload, Ask about Mathematics')
with st.sidebar:
    mode=st.radio('Choose Mode',options=['Draw','Upload','Chat'])
    if mode=='Draw':
        st.write('Instructions\n1. Draw or write something on canvas\n2. Click Solve Expression\n3. You will get your solution')
    if mode=='Upload':
        st.write('Instructions\n1. Upload an Image\n2. Click Solve Expression\n3. You will get your solution')
    if mode=='Chat':
        st.write('Instructions\n1. Ask chatbot about anything\n2. You will get your solution')
def get_gemini_model(api_key,model = 'gemini-2.5-flash'):
    try :
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model)
        return model,None
    except Exception as e:
        return None ,str(e)
def get_question():
    ques = input("enter : ")
    model,a = get_gemini_model(API_Key)
    if model:
        res = model.generate_content([ques])   
        print(res.text) 
if mode=='Chat':
    get_gemini_model('GOOGLE_API_KEY')
    get_question

