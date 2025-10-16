import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('myapp/config.yaml') as file:
    config=yaml.load(file,Loader=SafeLoader)
    
authenticator=stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def login_register():

    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status']=False
    if 'show_register' not in st.session_state:
        st.session_state['show_register']=False
        

    if not st.session_state.get('authentication_status'):
        
        with st.sidebar:
            if st.button('login'):
                st.session_state['show_register']=False
            if st.button('register'):
                st.session_state['show_register']=True
                
        
        if not st.session_state['show_register']:
            try:
                if authenticator.login():
                    st.success('login successfull')
                    if not st.session_state['authentication_status']:
                        st.error('invalid credentials')
                
            except Exception as e:
                st.error(str(e))
                
                
        if st.session_state['show_register']:   
            try:
                email,username,name=authenticator.register_user(password_hint=False,captcha=False)
                if email and username:
                    st.success('successfully Registered')
                    
                    with open('myapp/config.yaml','w') as file:
                        yaml.dump(config,file,default_flow_style=False)
                    st.session_state['show_register']=False
                    
            except Exception as e:
                st.error(str(e))
            
    if st.session_state['authentication_status']:
        with st.sidebar:
        #     st.write(f'welcome {config['credentials']['usernames'][st.session_state.get('username')]['first_name']}')
            authenticator.logout()
        

