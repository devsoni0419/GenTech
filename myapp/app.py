import streamlit as st
from streamlit_drawable_canvas import st_canvas
import login
# st.header('AI MATHEMATICS ASSISTANT')
login.login_register()
if st.session_state['authentication_status']:
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
        

            


