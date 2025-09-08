import streamlit as st, logging, time, base64
from PIL import Image, ImageEnhance
from src.agent_component.graph_builder import build_insurance_agent_graph 
from streamlit_pills import pills

# Configure logging
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Bajaj Allianz Insurance AI Assistant",
    page_icon="static/img/bajaj_logo.png",
    layout="wide",
)

# Constants
NUMBER_OF_MESSAGES_TO_DISPLAY = 20
USER_ICON = "static/img/stuser.png"
ASSISTANT_ICON = "static/img/stassisstant.png"
TEMPLATES = [
    "What is the Aapke Liye health insurance plan for my state?",
    "Show me the Mee Kosam plan brochure and policy details for Andhra Pradesh",
    "What documents do I need for Nimagagi health insurance proposal in Karnataka?",
    "How do I download the policy wordings for Aponar Babe plan in Assam?",
    "What are the benefits covered under Tuhade Lai Punjab health plan?",
    "Compare Aapke Liye plans for Uttar Pradesh vs Madhya Pradesh",
    "Where can I find the Customer Information Sheet for my regional plan?",
    "What is the difference between brochure and prospectus documents?",
    "How to fill the digital proposal form for Ungalukkaga Tamil Nadu plan?",
    "Show me all available documents for Ningalkkayi Kerala health insurance",
    "What regional language options are available for insurance documents?",
    "Explain the Tujya Khatir Goa plan coverage and exclusions",
    "How do I get the policy wordings in my local language?",
    "What is covered under Adomgidamak Manipur health insurance plan?",
    "Where can I download the latest proposal form for my state plan?"
]

st.markdown("""
    <style>
        [data-testid="stHeader"] {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background-color: transparent;
            
        }

        /* Push rest of the app content down to avoid being hidden behind fixed header */
        .block-container {
            padding-top: 0rem; /* adjust based on header height */
        }

        /* Bajaj Allianz Brand Colors */
        .bajaj-blue {
            color: #0056b3;
        }
        
        .bajaj-orange {
            color: #ff6600;
        }
    </style>
""", unsafe_allow_html=True)


# Streamlit Title with Bajaj Allianz branding
st.title("🛡️ Bajaj Allianz Insurance AI Assistant")
st.header("🏥 Get instant help with health insurance 💼, claims guidance 📋, and policy information 📑")


def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logging.error(f"Error converting image to base64: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def long_running_task(duration):
    """
    Simulates a long-running operation.

    Parameters:
    - duration: int, duration of the task in seconds

    Returns:
    - str: Completion message
    """
    time.sleep(duration)
    return "Long-running operation completed."

@st.cache_data(show_spinner=False)
def load_and_enhance_image(image_path, enhance=False):
    """
    Load and optionally enhance an image.

    Parameters:
    - image_path: str, path of the image
    - enhance: bool, whether to enhance the image or not

    Returns:
    - img: PIL.Image.Image, (enhanced) image
    """
    img = Image.open(image_path)
    if enhance:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.8)
    return img


@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input):
    """
    Handle chat input submissions and interact with the Insurance AI Agent.

    Parameters:
    - chat_input (str): The chat input from the user.

    Returns:
    - None: Updates the chat history in Streamlit's session state.
    """
    user_input = chat_input.strip()

    try:
        agent = build_insurance_agent_graph()
        response = agent.invoke(
            {
                "query": user_input
            }
        )
        # Here comes insurance assistant code
        assistant_reply = response["messages"][-1].content

        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        st.error(f"Error occurred: {str(e)}")



def initialize_session_state():
    """Initialize session state variables."""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "insurance_agent" not in st.session_state:
        st.session_state.insurance_agent = build_insurance_agent_graph()
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""



def stream_message():
    
    for message , metadata in st.session_state.insurance_agent.stream(
        {
            "query":st.session_state.chat_input
        },
        stream_mode="messages"
        
    ):
        if metadata['langgraph_node'] == "insurance_agent":
            yield message.content
    
                

def main():
    """
    Display Streamlit updates and handle the chat interface for Bajaj Allianz Insurance.
    """
    
    st.markdown(
        """
        <style>
        .cover-glow {
            width: 120px; /* 👈 shrink logo */
            height: auto;
            padding: 2px;
            margin: 10px auto;
            display: block;
            box-shadow: 
                0 0 6px #0056b3,
                0 0 12px #ff6600,
                0 0 18px #0066cc,
                0 0 24px #ff7733;
            border-radius: 25px;
            background-color: transparent;
        }
        [data-testid=stSidebar] {
                background-color: #0056b3;
        }

        /* Style the sidebar collapse (minimize) arrow */
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseControl"] svg {
            stroke: #ccc !important;
        }

        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            padding: 10px 20px;
            font-size: 14px;
            color: #666;
            text-align: right;
            z-index: 9999;
        }

        .footer p {
            margin: 0;
            padding: 0px 0;  /* Reduced padding between paragraphs */
        }
        </style>

        <div class="footer">
            <p> ⚠️ Disclaimer: AI-generated information for guidance only. Consult official Bajaj Allianz representatives for policy details | © 2025 <strong>Bajaj Allianz Insurance AI Assistant</strong> | IRDAI Reg. No. 113 | <strong><a href="https://www.bajajallianz.com/" target="_blank" style="color:inherit;text-decoration:underline;">Official Website</a></strong> </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load and display sidebar image (Bajaj Allianz logo)
    img_path = "static/img/bajaj_assistant.png" 
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'''
            <a href="https://www.bajajallianz.com/" target="_blank">
                <img src="data:image/png;base64,{img_base64}" class="cover-glow" />
            </a>
            ''',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='color: #ccc;'>
            <h1>🛡️ Bajaj Allianz Insurance</h1>
            Your <b>trusted insurance companion</b> available 24/7! Get instant answers about <b>health insurance policies</b>, <b>claim procedures</b>, and <b>coverage details</b>. 
            Whether you're looking to <b>buy new insurance</b>, <b>file a claim</b>, or <b>understand your policy</b>, our AI assistant provides you with <b>accurate information</b> and <b>step-by-step guidance</b> - all through simple conversations. 
            Make <b>informed insurance decisions</b> with confidence, backed by Bajaj Allianz's expertise and commitment to customer service.
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='color: #ccc;'>
            <h3>🎯 What You'll Achieve</h3>
            <ul>
                <li><b>🏥 Choose the Right Health Plan</b> - Compare different health insurance policies like My Health Care Plan, Health Guard Gold, and Health Infinity with detailed feature analysis.</li>
                <li><b>⚡ Fast Claim Processing Help</b> - Get step-by-step guidance for filing claims, understanding required documents, and tracking your claim status.</li>
                <li><b>📊 Understand Policy Benefits</b> - Clear explanations of coverage limits, exclusions, waiting periods, and special benefits for each insurance plan.</li>
                <li><b>📞 Quick Contact Information</b> - Instant access to customer service numbers, branch locations, and emergency contact details.</li>
                <li><b>🧠 Decode Insurance Terms</b> - Simple explanations of complex insurance terminology and policy conditions.</li>
                <li><b>💡 Personalized Recommendations</b> - Get suggestions based on your specific needs, age group, and health requirements.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='color: #ccc;'>
            <h3>🚀 Powerful Features</h3>
            <ul>
                <li><b>🤖 Smart Insurance Assistant</b> - Ask questions in natural language about any Bajaj Allianz insurance product and get detailed, accurate responses.</li>
                <li><b>🏥 Health Plan Expertise</b> - Comprehensive knowledge of all health insurance plans including My Health Care, Health Guard, Health Infinity, and specialized plans.</li>
                <li><b>📋 Claims Guidance</b> - Step-by-step claim process help, document checklists, and reimbursement procedure explanations.</li>
                <li><b>📑 Policy Documentation</b> - Access information about policy wordings, brochures, proposal forms, and important documents.</li>
                <li><b>🔄 Multi-Service Coverage</b> - Information about health, motor, travel, home, and other general insurance products.</li>
                <li><b>🧠 Advanced AI Reasoning</b> - Powered by sophisticated language models for accurate insurance advice and policy interpretations.</li>
                <li><b>💾 Session Memory</b> - Maintains context throughout your conversation for more personalized and relevant insurance guidance.</li>
                <li><b>📝 Detailed Explanations</b> - Get comprehensive information formatted for easy understanding and reference.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='color: #ccc;'>
            <h3>🔗 Quick Links</h3>
            <ul>
                <li><b>📞 Customer Care:</b> 1800-210-1030</li>
                <li><b>🌐 Official Website:</b> <a href="https://www.bajajallianz.com" target="_blank" style="color: #ff6600;">bajajallianz.com</a></li>
                <li><b>📱 Mobile App:</b> Caringly Yours</li>
                <li><b>📧 Email Support:</b> Available through official website</li>
                <li><b>🏢 IRDAI Reg. No.:</b> 113</li>
                <li><b>⚖️ Claim Settlement Ratio:</b> 90.64% (FY 2021-22)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)


    initialize_session_state()

    if not st.session_state.history:
        initial_bot_message = "Hello! I am your Bajaj Allianz Insurance Assistant. How can I help you with your insurance needs today? 🛡️"
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})

    # Display Templates 
    selected = pills(
        "Quick insurance queries:",
        TEMPLATES,
        clearable=True,
        index=None,
    )

    # Display chat input sections
    chat_in = st.chat_input("Ask me about Bajaj Allianz insurance plans, claims, or any insurance-related questions")

    # Display chat history
    for msg in st.session_state.history:
        avatar = ASSISTANT_ICON if msg["role"]=="assistant" else USER_ICON
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    st.session_state.chat_input = (
        chat_in if chat_in else
        selected if selected else
        None
    )
    
  
    # st.session_state.chat_input = (
    #     selected
    #     if selected
    #     else chat_in
    #     if chat_in
    #     else None
    # )        

    if st.session_state.chat_input:
        st.session_state.history.append(
            {
                "role": "user", 
                "content": st.session_state.chat_input 
            }
        )
        with st.chat_message("user", avatar=USER_ICON):
            st.write(st.session_state.chat_input )
        
        try:
            with st.chat_message("assistant", avatar=ASSISTANT_ICON):
                assistant_reply = st.write_stream(stream_message)
            
            st.session_state.history.append(
                {
                    "role": "assistant", 
                    "content": assistant_reply
                }
            )
            
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            st.error(f"Error in application: {str(e)}")


if __name__ == "__main__":
    main()