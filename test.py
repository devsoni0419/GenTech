import imghdr
from turtle import mode
import streamlit as st
from PIL import Image
import google.generativeai as genai
from GenTech.API_KEY import API_Key


st.header("AI chatBot")
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

    if isPil:
        img_data =img_data.convert('RGB') 
    else :
        img = Image.fromarray(img_data.astype('uInt8'),'RGBA')
        img_new = Image.new('RGB',img.size,(255,255,255))
        img.paste(img_new,mask = img.split()[3])
        img_data = img
    
    img_data.show


# get_gemini_model(API_Key)
with open(r'C:\Users\WELCOME\OneDrive\Documents\.jpg\photosunny.jpg','rb') as f:
    img = Image.open(f,'r')
print(type(img))
get_image_response(img)
# print(genai.configure())
# get_question()

