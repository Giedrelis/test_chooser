import streamlit as st
import json

# Load the decision tree from the JSON file
try:
    with open("decision_tree.json", "r", encoding="utf-8") as file:
        DECISION_TREE = json.load(file)
except FileNotFoundError:
    st.error("The decision_tree.json file was not found.")
    st.stop()
except json.JSONDecodeError:
    st.error("Invalid JSON format in decision_tree.json.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

# Load the tests descriptions from the JSON file
try:
    with open("tests.json", "r", encoding="utf-8") as file:
        TESTS = json.load(file)
except FileNotFoundError:
    st.error("The tests.json file was not found.")
    st.stop()
except json.JSONDecodeError:
    st.error("Invalid JSON format in tests.json.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

def get_next_node(node_id, tree):
    """
    Retrieve the node with the given ID from the decision tree.
    """
    for node in tree:
        if node["id"] == node_id:
            return node
        if "nodes" in node:
            next_node = get_next_node(node_id, node["nodes"])
            if next_node:
                return next_node
    return None

def chat_with_tree():
    """
    Chat with the user based on the decision tree.
    """
    st.title("ČekanavičiusGPT")

    # Apply custom styles
    st.markdown("""
        <style>
            .stChat .stChatMessage p {
                font-size: 20px;
            }
            .stButton>button {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # Initialize or retrieve the current node and chat history from session state
    if "current_node" not in st.session_state:
        st.session_state.current_node = DECISION_TREE
        st.session_state.chat_history = []
        st.session_state.chat_history.append({"name": "assistant", "text": DECISION_TREE["question"]})
        if "comments" in DECISION_TREE and DECISION_TREE["comments"].strip():
            st.session_state.chat_history.append({"name": "assistant", "text": DECISION_TREE["comments"]})
    current_node = st.session_state.current_node

    # Display the chat history
    for message in st.session_state.chat_history:
        with st.chat_message(name=message["name"]):
            st.write(message["text"])

    # Display the available answers as buttons
    selected_option = None
    for option in [answer["text"] for answer in current_node["answers"]]:
        if st.button(option):
            selected_option = option
            break

    if selected_option:
        with st.chat_message("user"):
            st.write(selected_option)

        # Add the selected answer to the chat history
        st.session_state.chat_history.append({"name": "user", "text": selected_option})

        # Find the selected answer
        for answer in current_node["answers"]:
            if answer["text"] == selected_option:
                if "action" in answer:
                    with st.chat_message(name="assistant"):
                        st.write(answer["action"])
                    # Add the action to the chat history
                    st.session_state.chat_history.append({"name": "assistant", "text": answer["action"]})
                elif "next" in answer:
                    next_node = get_next_node(answer["next"], [DECISION_TREE])
                    st.session_state.chat_history.append({"name": "assistant", "text": next_node["question"]})
                    if "comments" in next_node and next_node["comments"].strip():
                        st.session_state.chat_history.append({"name": "assistant", "text": next_node["comments"]})
                    st.session_state.current_node = next_node
                    st.experimental_rerun()

        # Display the test description if available
        if "test" in current_node and current_node["test"] in TESTS:
            st.sidebar.markdown(TESTS[current_node["test"]])

    # Reset button on the bottom right, always visible
    cols = st.columns([4, 1])
    with cols[1]:
        if st.button("Iš naujo", type="primary"):
            if "current_node" in st.session_state:
                del st.session_state.current_node
            if "chat_history" in st.session_state:
                del st.session_state.chat_history
            st.experimental_rerun()

def main():
    chat_with_tree()

if __name__== "__main__":
    main()
