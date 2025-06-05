import streamlit as st
import re
import pandas as pd

# ---- Streamlit page setup ----
st.set_page_config(page_title="BuyerHunter AI", page_icon="🏠")

st.title("🏠 BuyerHunter AI")
st.write(
    "Automatically extract real estate buyer contact numbers and names from text. "
    "Paste WhatsApp chats, listings, or comments and click 'Extract Buyers'."
)

# ---- User Input ----
input_text = st.text_area(
    "Paste text, listings, or comments here:",
    height=200,
    placeholder="Paste your real estate leads or WhatsApp chats here..."
)

# ---- Extraction Functions ----
def extract_phone_numbers(text):
    # Matches Indian phone numbers, optionally with +91
    phone_pattern = re.compile(r'(?:\+91[\-\s]?)?[6-9]\d{9}')
    return phone_pattern.findall(text)

def extract_names(text):
    # Looks for capitalized words of length >=3 (very basic, can be improved)
    # Excludes common real estate terms and city names (expandable)
    common_words = set([
        "Flat", "House", "Apartment", "Land", "Plot", "Contact", "Owner", "Agent",
        "Buy", "Sell", "Rent", "Available", "Requirement", "Looking", "BHK", "Sqft"
    ])
    words = set(re.findall(r'\b[A-Z][a-z]{2,}\b', text))
    names = [w for w in words if w not in common_words]
    return names

# ---- Main Extraction Logic ----
if st.button("Extract Buyers"):
    if not input_text.strip():
        st.error("Please paste some text above!")
    else:
        phones = extract_phone_numbers(input_text)
        names = extract_names(input_text)

        # --- Display Phones ---
        if not phones:
            st.warning("No phone numbers found!")
        else:
            st.success(f"Found {len(phones)} phone number(s).")
            df = pd.DataFrame({'Phone Number': phones})
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='buyer_contacts.csv',
                mime='text/csv',
            )

        # --- Display Names ---
        if names:
            st.write("**Possible Buyer Names found:**")
            st.write(", ".join(names))
        else:
            st.info("No clear buyer names detected.")

# ---- Footer ----
st.markdown("---")
st.write("Made by [Home Star Realty](https://www.homestarrealty.in) | Shivam Mishra")