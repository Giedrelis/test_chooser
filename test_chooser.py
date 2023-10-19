import streamlit as st
import json

# Load the decision tree from the JSON file
@st.cache
def load_decision_tree():
    with open('decision_tree.json', 'r') as file:
        return json.load(file)

decision_tree = load_decision_tree()

# Recursive function to navigate through the decision tree
def navigate_tree(node):
    # Display the question
    st.write(node["question"])

    # If there's a comment, display it
    if "comments" in node:
        st.write(node["comments"])

    # Display the answers as buttons
    answer = st.radio("", [ans["text"] for ans in node["answers"]])

    # Find the selected answer
    for ans in node["answers"]:
        if ans["text"] == answer:
            selected_answer = ans
            break

    # If the selected answer has an action, display it
    if "action" in selected_answer:
        st.write(selected_answer["action"])
        if "interpretation" in selected_answer:
            st.write(selected_answer["interpretation"])

    # If the selected answer leads to another node, navigate to that node
    elif "next" in selected_answer:
        next_node_id = selected_answer["next"]
        for next_node in node.get("nodes", []):
            if next_node["id"] == next_node_id:
                navigate_tree(next_node)
                break

def main():
    st.title("ČekanavičiusGPT")
    navigate_tree(decision_tree)

if __name__ == "__main__":
    main()
