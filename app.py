import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="NFA to DFA Converter", page_icon="🗿", layout="centered")

st.title("NFA to DFA & Strict Password Validator 🗿")

st.divider()


# NFA to DFA
def convert_nfa_to_dfa(nfa, nfa_final_states):
    new_states = []
    dfa = {}
    initial_state = list(nfa.keys())[0]
    transition_symbols = list(nfa[initial_state].keys())

    dfa[initial_state] = {}
    for symbol in transition_symbols:
        next_states = "".join(nfa[initial_state][symbol])
        dfa[initial_state][symbol] = next_states
        if next_states not in dfa:
            new_states.append(next_states)
            dfa[next_states] = {}

    while new_states:
        current_state = new_states.pop(0)
        for symbol in transition_symbols:
            next_states = []
            for char in current_state:
                next_states.extend(nfa[char].get(symbol, []))
            next_state_str = "".join(next_states)
            if next_state_str not in dfa:
                new_states.append(next_state_str)
                dfa[next_state_str] = {}
            dfa[current_state][symbol] = next_state_str

    dfa_final_states = [
        state for state in dfa if any(char in nfa_final_states for char in state)
    ]

    return dfa, dfa_final_states


st.header("NFA to DFA Converter")

num_states = st.number_input("Number of states", min_value=1, step=1)
num_transitions = st.number_input("Number of alphabets", min_value=1, step=1)

nfa = {}

for i in range(num_states):
    state_name = st.text_input(
        f"State name {i + 1}", key=f"state_{i}", placeholder=f"State name {i + 1}"
    )
    nfa[state_name] = {}
    for j in range(num_transitions):
        transition_symbol = st.text_input(
            f"Alphabet from state {state_name} ({i + 1}-{j + 1})",
            key=f"symbol_{i}_{j}",
            placeholder=f"Alphabet from state {state_name} ({i + 1}-{j + 1})",
        )
        reaching_states = st.text_input(
            f"End state(s) from {state_name} traveling through {transition_symbol} (space-separated if more than 1)",
            key=f"reaching_states_{i}_{j}",
            placeholder=f"End state(s) from {state_name} traveling through {transition_symbol} (space-separated if more than 1)",
        )
        nfa[state_name][transition_symbol] = reaching_states.split()

nfa_table = pd.DataFrame(nfa).transpose()
st.write("NFA Table")
st.write(nfa_table)

nfa_final_states_input = st.text_input(
    "Enter final states of NFA (space-separated if more than 1)",
    key="nfa_final_states",
    placeholder="Enter final states of NFA (space-separated if more than 1)",
)
nfa_final_states = nfa_final_states_input.split()

if st.button("Convert to DFA"):
    dfa, dfa_final_states = convert_nfa_to_dfa(nfa, nfa_final_states)
    dfa_table = pd.DataFrame(dfa).transpose()
    st.write("DFA Table")
    st.write(dfa_table)
    st.write("Final states of the DFA")
    st.write(dfa_final_states)


# Password Validator


def clean_username(username):
    filtered = "".join(filter(str.isalpha, username))
    return "".join(
        char for i, char in enumerate(filtered) if i == 0 or char != filtered[i - 1]
    ).lower()


st.header("Strict Password Validator")

st.info(
    """
Password Requirements:
- Must not contain the username.\n
- Must contain at least 1 uppercase letter.\n
- Must contain at least 1 lowercase letter.\n
- Must contain at least 1 number (0-9).\n
- Must contain at least 1 special character.\n
- No spaces allowed.\n
- Length must be greater than 12 characters."""
)

if "credentials" not in st.session_state:
    st.session_state.credentials = []

username = st.text_input("Enter your username", placeholder="Enter your username")
password = st.text_input(
    "Enter your password", type="password", placeholder="Enter your password"
)

password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s])[\S]{13,}$"

if st.button("Check"):
    if not password.strip():
        st.warning("Please enter a password before clicking the button.")
    else:
        if clean_username(username) in clean_username(password):
            st.error(
                "Your password contains the username, hence it can not be set. Try again!"
            )
        elif re.fullmatch(password_pattern, password):
            st.success(
                "Your password has been set and is very strong!\n\n"
                "It would take an estimated over 15 million years to crack such a password with a brute force attack, "
                "assuming the criteria are strictly followed and the cracking speed remains constant."
            )
            st.session_state.credentials.append(
                {"Username": username, "Password": password}
            )
        else:
            st.error("Your password does not meet the required criteria. Try again!")

if st.session_state.credentials:
    st.subheader("Stored Usernames and Passwords")
    credentials_df = pd.DataFrame(st.session_state.credentials)
    st.dataframe(credentials_df)

st.markdown(
    "<h5 style='text-align: center;'>made by Fahad | Uzair | Raza</h5>",
    unsafe_allow_html=True,
)
