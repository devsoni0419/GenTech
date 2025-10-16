import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import google.generativeai as genai
import io
import json 
from API_KEY import API_Key
# import login


st.set_page_config(page_title="AI Math Assistant", layout="wide")


st.markdown("""
<style>
header[data-testid="stHeader"] {
    background-color: #1A1A3D; /* Dark Navy */
    height: 70px;
    color: #33E6F6; /* Electric Blue */
    text-align: center;
    position: relative;
    border-bottom: 2px solid #33E6F6; /* Electric Blue Border */
}
header[data-testid="stHeader"]::after {
    content: "AI-Powered Math Assistant";
    position: absolute;
    top: 30%;
    left: 50%;
    transform: translate(-50%, -25%);
    font-size: 2rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# login.login_register()



# if st.session_state['authentication_status']:



st.markdown("<h1 style='color:#33E6F6'>Draw, upload, or chat about math problems!</h1>",unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'solution_result' not in st.session_state: 
    st.session_state.solution_result = None
if 'feedback_given' not in st.session_state: 
    st.session_state.feedback_given = None
if 'canvas_clear_key' not in st.session_state:
    st.session_state.canvas_clear_key = 0
if 'previous_mode' not in st.session_state:
    st.session_state.previous_mode = None

def clear_solution_state():
    st.session_state.solution_result = None
    st.session_state.feedback_given = None

with st.sidebar:
    api_key = API_Key
    st.markdown("---")
    st.header(" Mode")
    mode = st.radio(
        "Choose input mode:",
        ["Draw", "Upload Image", "Chat"],
        label_visibility="collapsed"
    )

    if st.session_state.previous_mode is None:
        st.session_state.previous_mode = mode
    if st.session_state.previous_mode != mode:
        clear_solution_state()
        st.session_state.previous_mode = mode
        
    st.markdown("---")
    st.markdown(" Instructions")
    if mode == "Draw":
        st.markdown("1. Draw an expression\n2. Click 'Solve'\n3. Get the solution!")
    elif mode == "Upload Image":
        st.markdown("1. Upload an image\n2. Click 'Solve'\n3. Get the solution!")
    
    
    if mode == "Chat":
        def clear_chat_history():
            st.session_state.messages = []
            st.session_state.chat_session = None
        
        st.button("Clear Chat History", on_click=clear_chat_history, use_container_width=True)

    st.markdown("---")

def get_gemini_model(api_key, model_name='gemini-2.0-flash-exp'):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        return model, None
    except Exception as e:
        return None, str(e)

def solve_with_gemini(image_data, api_key, is_pil=False):
    model, error = get_gemini_model(api_key)
    if error: return f"Error initializing model: {error}"
    try:
        if is_pil: rgb_img = image_data.convert('RGB')
        else:
            img = Image.fromarray(image_data.astype('uint8'), 'RGBA')
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
        prompt = """Analyze this mathematical expression. Solve it step-by-step and provide a final answer in the format: **Answer:** [final answer]"""
        response = model.generate_content([prompt, rgb_img])
        return response.text
    except Exception as e: return f"Error: {str(e)}"

def get_chat_session(api_key):
    if 'chat_session' not in st.session_state or st.session_state.chat_session is None:
        try:
            model, error = get_gemini_model(api_key)
            if error:
                st.error(f"Error initializing chat: {error}")
                return None
            st.session_state.chat_session = model.start_chat(history=[])
        except Exception as e:
            st.error(f"Error initializing chat: {str(e)}")
            return None
    return st.session_state.chat_session

def generate_quiz(topic, difficulty, api_key):
    model, error = get_gemini_model(api_key)
    if error:
        st.error(f"Error initializing model for quiz: {error}")
        return None
    prompt = f"""You are a quiz generator. Create a 5-question multiple-choice quiz about {topic} at a {difficulty} level. Return the quiz as a valid JSON list. Each object must have keys: "question", "options" (a list of 4 strings), and "answer" (the correct option string). Do not include any text before or after the JSON list."""
    try:
        with st.spinner(f"Generating a {difficulty} {topic} quiz..."):
            response = model.generate_content(prompt)
            json_text = response.text.strip().replace("```json", "").replace("```", "")
            questions = json.loads(json_text)
            return questions
    except Exception as e:
        st.error(f"Failed to generate or parse quiz. Error: {e}")
        return None




if mode == "Chat":
    st.subheader("Math Chat Assistant")
    st.markdown("""
    <style>
        [data-testid="stChatInput"] {
            bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.write("Hello! How can I help you with your math problems today? 🤖")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("Ask me anything about math..."):
        if not api_key: st.error("Please enter your Gemini API key!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    chat = get_chat_session(api_key)
                    response = chat.send_message(f"You are a helpful math tutor developed by O(1) Squad. The members are Dev Soni(Leader), Sunny Yadav, Rishi Bisht. Help with: {prompt}")
                    response_text = response.text
                st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})


else:
    if mode == "Draw":
        st.subheader("Draw Your Expression")
        canvas_col, controls_col = st.columns([2, 1])
        
        with controls_col:
            st.markdown("#### Drawing Controls")
            stroke_width = st.slider("Stroke width:", 1, 50, 3)
            stroke_color_choice = st.color_picker("Stroke color:", "#33E6F6") # Electric Blue
            bg_color = st.color_picker("Background:", "#1A1A3D") # Dark Navy Canvas
            drawing_tool_choice = st.selectbox("Drawing tool:", ("freedraw", "line", "rect", "circle", "transform"))
            use_eraser = st.checkbox("Use Eraser")
            if use_eraser:
                final_stroke_color = bg_color
                final_drawing_tool = "freedraw"
            else:
                final_stroke_color = stroke_color_choice
                final_drawing_tool = drawing_tool_choice
            def clear_canvas(): st.session_state.canvas_clear_key += 1
            st.button("Clear Canvas", use_container_width=True, on_click=clear_canvas)
        
        
        with canvas_col:
            canvas_result = st_canvas(
                stroke_width=stroke_width,
                stroke_color=final_stroke_color,
                background_color=bg_color,
                height=605,
                width=1200,
                drawing_mode=final_drawing_tool,
                display_toolbar=False,
                key=f"canvas_{st.session_state.canvas_clear_key}"
            )
        image_to_process = canvas_result.image_data if canvas_result.image_data is not None else None
        is_pil = False

    else: 
        st.subheader("Upload Math Problem Image")
        uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg"], on_change=clear_solution_state)
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            image_to_process = image; is_pil = True
        else:
            image_to_process = None; is_pil = False
    
    st.markdown("---")

    if st.button("Solve Expression", type="primary", use_container_width=True):
        if not api_key: st.error("Please enter your Gemini API key!")
        elif image_to_process is None: st.warning(f"Please {'draw' if mode == 'Draw' else 'upload an image'} first!")
        else:
            with st.spinner("Analyzing your image..."):
                st.session_state.solution_result = solve_with_gemini(image_to_process, api_key, is_pil)
                st.session_state.feedback_given = None
            st.rerun()

    st.markdown("---")
    
    st.subheader("AI Solution")
    result_container = st.container(height=500, border=True)

    if st.session_state.solution_result:
        with result_container:
            st.markdown(st.session_state.solution_result)
            if not st.session_state.feedback_given:
                st.info("Please verify the solution. AI can make mistakes.", )
                feedback_cols = st.columns(2)
                with feedback_cols[0]:
                    if st.button("Correct", use_container_width=True):
                        st.session_state.feedback_given = 'correct'
                        st.rerun()
                with feedback_cols[1]:
                    if st.button("Incorrect", use_container_width=True):
                        st.session_state.feedback_given = 'incorrect'
                        st.rerun()
            elif st.session_state.feedback_given == 'correct':
                st.success("Great! Analysis complete.")
                if st.button("Continue this in chat mode"):
                    st.session_state.messages.append({"role": "assistant", "content": f"I just solved this problem:\n\n{st.session_state.solution_result}"})
                    st.info("Added to chat history! Switch to 'Chat' mode to continue.")
            elif st.session_state.feedback_given == 'incorrect':
                st.warning("Thanks for the feedback! We'll use this to improve.")
            
            st.button("Clear AI Solution", use_container_width=True, on_click=clear_solution_state)

if mode != "Chat":
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #8F8FA3;'> <p>Powered by Google Gemini 2.0 Flash </p>
        <p><small>Tip: Write clearly or upload high-quality images for best results!</small></p>
    </div>
    """, unsafe_allow_html=True)
