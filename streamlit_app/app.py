import streamlit as st, logging, time, base64
from PIL import Image, ImageEnhance
from src.agent_component.graph_builder import build_insurance_agent_graph 
from streamlit_pills import pills

# Configure logging
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Financial AI Agent",
    page_icon="static/img/stassisstant.png",
    layout="wide",
)

# Constants
NUMBER_OF_MESSAGES_TO_DISPLAY = 20
USER_ICON = "static/img/stuser.png"
ASSISTANT_ICON = "static/img/stassisstant.png"
TEMPLATES = [
    "How risky is it to invest in Nvidia(NVDA) right now?",
    "What's the 10-day stock trend for Apple?",
    "What are the latest analyst recommendations for Samsung (SSNLFA)?",
    "Show me the stock price, compony info and ,analyst recommendation for Amazon(AMZN)",
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
    </style>
""", unsafe_allow_html=True)


# Streamlit Title
st.title("💹 Financial AI Agent Assistant")
st.header("📊 Get smart financial insights 💡, real-time stock data 📈, and news-driven analysis 📰")


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
    Handle chat input submissions and interact with the OpenAI API.

    Parameters:
    - chat_input (str): The chat input from the user.

    Returns:
    - None: Updates the chat history in Streamlit's session state.
    """
    user_input = chat_input.strip().lower()

    try:
        agent = build_insurance_agent_graph()
        response = agent.invoke(
            {
                "query": user_input
            }
        )
        # Here comess assitant code
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
    if "finance_agent" not in st.session_state:
        st.session_state.finance_agent = build_insurance_agent_graph()
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""



def stream_message():
    
    for message , metadata in st.session_state.finance_agent.stream(
        {
            "query":st.session_state.chat_input
        },
        stream_mode="messages"
        
    ):
        if metadata['langgraph_step'] == 1 and message.content != "":
            yield message.content

        if metadata['langgraph_step'] != 1 and metadata['langgraph_node'] == "reasoner":
            yield message.content
    
                

def main():
    """
    Display Streamlit updates and handle the chat interface.
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
                0 0 6px #2f3b91,
                0 0 12px #3f4ec9,
                0 0 18px #5f6be0,
                0 0 24px #7f89f2;
            border-radius: 25px;
            background-color: transparent;
        }
        [data-testid=stSidebar] {
                background-color: #1e3a8a;
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
            <p> ⚠️ Disclaimer: AI-generated insights for informational purposes only. Consult financial experts before investing | © 2025 <strong>Financial AI Agent</strong> | Powered by <strong><a href="https://www.dziretechnologies.com/" target="_blank" style="color:inherit;text-decoration:underline;">Dzire Technologies</a></strong> </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load and display sidebar image
    img_path = "static/img/stassisstant.png" 
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'''
            <a href="https://www.dziretechnologies.com/" target="_blank">
                <img src="data:image/png;base64,{img_base64}" class="cover-glow" />
            </a>
            ''',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='color: #ccc;'>
            <h1>💹 Financial AI Agent</h1>
            You're <b>personal Financial advisor</b> that never sleeps! Get instant answers to all your investment questions, from stock performance to market trends. 
            Whether you're a <b>beginner investor</b> or a <b>seasoned trader</b>, our AI assistant provides you with <b>real-time market data</b>, <b>expert-level analysis</b>, and <b>breaking financial news</b> - all through simple conversations. 
            Make <b>smarter investment decisions</b> with confidence, backed by the same data that professional analysts use.
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='color: #ccc;'>
            <h3>🎯 What You'll Achieve</h3>
            <ul>
                <li><b>💰 Make Informed Investment Decisions</b> - Get comprehensive analysis with real-time stock data, news sentiment, and expert insights all in one place.</li>
                <li><b>⚡ Save Hours of Research Time</b> - No more jumping between multiple finance websites. Get everything you need through simple conversational queries.</li>
                <li><b>📊 Visualize Market Trends Instantly</b> - View stock performance through interactive charts and easy-to-read tables that highlight key metrics.</li>
                <li><b>🔍 Stay Ahead of Market News</b> - Get the latest financial news and analyst recommendations that could impact your investments.</li>
                <li><b>🧠 Understand Complex Financial Data</b> - Our AI breaks down complex market information into clear, actionable insights you can actually use.</li>
                <li><b>💡 Get Personalized Risk Assessments</b> - Understand the risk level of potential investments based on current market conditions and historical performance.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='color: #ccc;'>
            <h3>🚀 Powerful Features</h3>
            <ul>
                <li><b>🤖 Smart Conversational Interface</b> - Ask questions in natural language and get human-like responses with detailed explanations.</li>
                <li><b>📈 Real-Time Stock Data Integration</b> - Live stock prices, historical charts, and performance metrics directly from Yahoo Finance.</li>
                <li><b>📰 Context-Enriched News Analysis</b> - Get relevant financial news with AI-powered sentiment analysis and impact assessment.</li>
                <li><b>📊 Interactive Data Visualization</b> - View stock trends, growth charts, and comparison tables that make complex data easy to understand.</li>
                <li><b>🔄 Multi-Agent Coordination</b> - Our intelligent system uses specialized agents (Reasoner → Tool Agent) for comprehensive analysis.</li>
                <li><b>🧠 Advanced LLM Reasoning</b> - Powered by Groq-hosted LLaMA 3-70B for sophisticated financial analysis and recommendations.</li>
                <li><b>💾 Session Memory</b> - Maintains context throughout your conversation for more personalized and relevant responses.</li>
                <li><b>📝 Professional Report Generation</b> - Get well-formatted, markdown-based outputs perfect for sharing or saving.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)


    initialize_session_state()

    if not st.session_state.history:
        initial_bot_message = "Hello! I am Finance Assistant. How can I assist you with finance today?"
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})

    # Display Templates 
    selected = pills(
        "Quick prompts:",
        TEMPLATES,
        clearable=True,
        index=None,
    )

    # Display chat input sections
    chat_in = st.chat_input("Ask me about finance stocks related questions")

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