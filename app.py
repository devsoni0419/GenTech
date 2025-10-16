import streamlit as st
from streamlit_drawable_canvas import st_canvas
# st.header('AI MATHEMATICS ASSISTANT')
# import GenTech1.GenTech.myapp.login as log
# log.login_register()
# from loginn import login_register
# loginn.login_register()
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
        color:#F00
    }

</style>
'''
html='''
<style>
header[data-testid='stheader']{
    
        background-color:#000
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
with st.sidebar:
    mode=st.radio('Choose Mode',options=['Draw','Upload','Chat'])
    if mode=='Draw':
        st.write('Instructions\n1. Draw or write something on canvas\n2. Click Solve Expression\n3. You will get your solution')
    if mode=='Upload':
        st.write('Instructions\n1. Upload an Image\n2. Click Solve Expression\n3. You will get your solution')
    if mode=='Chat':
        st.write('Instructions\n1. Ask chatbot about anything\n2. You will get your solution')
if mode=='Draw':
    col1,col2=st.columns([2,1])
    with col2:
        strock=st.slider('Strock Width',1,25,3)
        color=st.color_picker('Strock Color',"#000")
        b_color=st.color_picker('Background Color','#FFF')
        erase=st.checkbox('Use Eraser')
    with col1:
        canvas=st_canvas( width='500px',
            height='500px',
            display_toolbar=False,
            stroke_width=strock,
            stroke_color=color,
            background_color=b_color,
        )
    
        
if mode=='Upload':
    image=st.file_uploader('Upload an image',type='jpg')
    
    
if mode=='Chat':
    get_session_
    


