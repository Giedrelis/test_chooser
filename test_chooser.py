import streamlit as st
import json

# Load the decision tree data
with open("decision_tree.json", "r") as file:
    DECISION_TREE = json.load(file)

# Recursive function to navigate through the decision tree
def navigate_tree(node):
    # Display the question
    with st.chat_message("assistant"):
        st.write(node["question"])

    # If there's a comment, display it
    if "comments" in node:
        with st.chat_message("assistant"):
            st.write(node["comments"])

    # Display the answer options
    options = [answer["text"] for answer in node["answers"]]
    choice = st.radio("", options)

    # Find the chosen answer
    for answer in node["answers"]:
        if answer["text"] == choice:
            # If there's an action, display it
            if "action" in answer:
                with st.chat_message("assistant"):
                    st.write(answer["action"])
            # If there's a next node, navigate to it
            elif "next" in answer:
                next_node_id = answer["next"]
                for next_node in node["nodes"]:
                    if next_node["id"] == next_node_id:
                        navigate_tree(next_node)
                        break

def main():
    st.title("ČekanavičiusGPT")
    navigate_tree(DECISION_TREE)
    if st.button("Iš naujo", key="reset"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()