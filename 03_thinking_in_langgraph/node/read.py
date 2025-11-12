from langchain_core.messages import HumanMessage
from state import EmailAgentState

def read_email(state: EmailAgentState) -> dict:
    """Extract and parse email content"""
    return {
        "messages": [HumanMessage(content=f"Processing email: {state['email_content']}")]
    }
