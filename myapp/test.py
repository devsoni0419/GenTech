import imghdr
from turtle import mode
import streamlit as st
from PIL import Image
import google.generativeai as genai
from API_KEY import API_Key
import numpy as np
from google.genai import types
from streamlit_drawable_canvas import st_canvas

html='''
<style>
header[data-testid='stheader']{
    
        background-color:#000
        color:#FFF
        
    }
header[data-testid='stheader']::after{
        content:'AI MATHEMATICS ASSISTANT'
        text-align:center
        top:0px
        color:#4F4DBD
    }

</style>
'''
html='''
<style>
header[data-testid='stheader']{
    
        background-color:#4F4DBD
        color:#FFF
    }
header[data-testid='stheader']::after{
        content:'AI MATHEMATICS ASSISTANT'
        text-align:center
    }

</style>
'''
st.html('<h1 style="margin:0" px>AI MATHEMATICS ASSISTANT</h1>')
st.markdown(html,unsafe_allow_html=True)
st.title('Draw,Upload, Ask about Mathematics')

    


# st.header("AI Mathematical Assitent")
if 'chat_session' not in st.session_state:
    st.session_state['chat_session'] = None
if 'quiz_session' not in st.session_state:
    st.session_state['quiz_session'] = []
if 'question_index' not in st.session_state:
    st.session_state['question_index'] = 0
# if 'quiz_session' not in st.session_state:
    st.session_state['quiz_session'] = []
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

def get_image_response(img_data,isPil = False):
    img_res = None
    if isPil:
        img_res = img_data.convert('RGB') 
    else :
        # image = types.Part.from_bytes(
        #    data=img_data, mime_type="image/jpeg"
        # )
        img = Image.fromarray(img_data.astype('uint8'),'RGBA')
        img_new = Image.new('RGB',img.size,(255,255,255))
        img.paste(img_new,mask = img.split()[3])
        img_res = img
        img_res.show()
    
    
    model ,error =get_gemini_model(API_Key)
    if error:
        return "Pleas fill API key"
    
    res = model.generate_content(['Analiysi the image if image constain any mathematic exparess,physics, solve this problem if not then Describe the image',img_res])
    ai = st.chat_message('ai')
    if st.spinner("Thinking"):
        ai.write(res.text)
        return None
def solve_with_gemini(image_data, api_key, is_pil=False):
        model, error = get_gemini_model(api_key)
        if error: return f" Error initializing model: {error}"
        try:
            if is_pil: rgb_img = image_data.convert('RGB')
            else:
                img = Image.fromarray(image_data.astype('uint8'), 'RGBA')
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
            prompt = """Analyze this mathematical expression. Solve it step-by-step and provide a final answer in the format: **Answer:** [final answer]"""
            response = model.generate_content([prompt, rgb_img])
            ai = st.chat_message('ai')
            if st.spinner("Thinking"):
                ai.write(response.text)
            return None
        except Exception as e: return f" Error: {str(e)}"

    
def get_chat_session():
    if not st.session_state['chat_session'] :
        

        promt =  st.chat_input("Ask Anything")
        if promt != None :
            model,error = get_gemini_model(API_Key)
            if error:
                return "Can't fetch api key"
            user = st.chat_message("user")
            user.write(promt)
            if st.spinner("Thinking"):
                res = model.generate_content([f"You are a AI math assistent ,and developed by O(1) squad where Team member is Leader (Dev soni),Sunn yadav,Rishi Bisht : give solution to the given Problem {promt}"])
                ai = st.chat_message("ai")
                ai.write(res.text)
    
def get_upload_session():
    
    st.markdown('# file upload ')

    file = st.file_uploader("upload file math problem",['jpg','jpeg'])
    if file:        
        if st.button('Analyze'):
            solve_with_gemini(file,API_Key)
                
def get_draw_session():           
   
        col1,col2=st.columns([2,1])
        with col2:
            strock=st.slider('Strock Width',1,25,3)
            color=st.color_picker('Strock Color',"#000")
            b_color=st.color_picker('Background Color','#4F4DBD')
            erase=st.checkbox('Use Eraser')
        with col1:
            canvas=st_canvas( width='500px',
                height='500px',
                display_toolbar=False,
                stroke_width=strock,
                stroke_color=color,
                background_color=b_color,
            )
        if st.button("Analysis image"):
            img = canvas.image_data if canvas.image_data is not None else None
            solve_with_gemini(img,API_Key)
            
        


with st.sidebar:
    mode=st.radio('Choose Mode',options=['Draw','Upload','Chat'])
    if mode=='Draw':
        st.write('Instructions\n1. Draw or write something on canvas\n2. Click Solve Expression\n3. You will get your solution')
    if mode=='Upload':
        st.write('Instructions\n1. Upload an Image\n2. Click Solve Expression\n3. You will get your solution')
    if mode=='Chat':
        # get_chat_session()
        st.write('Instructions\n1. Ask chatbot about anything\n2. You will get your solution')
if mode =='Chat':
    get_chat_session()
    # st.rerun()
elif mode == 'Upload':
    get_upload_session()
    # st.rerun()
elif mode == 'Draw':
    get_draw_session()
    # st.rerun()

