import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "tickets.csv"

# -------------------------
# Initialize data storage
# -------------------------
def load_tickets():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Ticket ID",
            "Title",
            "Description",
            "Priority",
            "Status",
            "Assigned To",
            "Created At"
        ])

def save_tickets(df):
    df.to_csv(DATA_FILE, index=False)

tickets = load_tickets()

st.set_page_config(page_title="Ticketing System", layout="wide")
st.title("🎫 Simple Ticketing System")

# -------------------------
# Sidebar Navigation
# -------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Create Ticket", "View Tickets", "Update Ticket"]
)

# -------------------------
# Create Ticket
# -------------------------
if menu == "Create Ticket":
    st.subheader("Create a New Ticket")

    title = st.text_input("Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    assigned_to = st.text_input("Assigned To (optional)")

    if st.button("Submit Ticket"):
        if title and description:
            new_ticket = {
                "Ticket ID": len(tickets) + 1,
                "Title": title,
                "Description": description,
                "Priority": priority,
                "Status": "Open",
                "Assigned To": assigned_to if assigned_to else "Unassigned",
                "Created At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            tickets = pd.concat([tickets, pd.DataFrame([new_ticket])])
            save_tickets(tickets)

            st.success("✅ Ticket created successfully!")
        else:
            st.error("⚠️ Title and Description are required.")

# -------------------------
# View Tickets
# -------------------------
elif menu == "View Tickets":
    st.subheader("All Tickets")

    if tickets.empty:
        st.info("No tickets found.")
    else:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Open", "In Progress", "Resolved", "Closed"]
        )

        filtered_tickets = tickets.copy()
        if status_filter != "All":
            filtered_tickets = filtered_tickets[
                filtered_tickets["Status"] == status_filter
            ]

        st.dataframe(filtered_tickets, use_container_width=True)

# -------------------------
# Update Ticket
# -------------------------
elif menu == "Update Ticket":
    st.subheader("Update Ticket")

    if tickets.empty:
        st.info("No tickets available.")
    else:
        ticket_id = st.selectbox(
            "Select Ticket ID",
            tickets["Ticket ID"].tolist()
        )

        ticket = tickets[tickets["Ticket ID"] == ticket_id].iloc[0]

        new_status = st.selectbox(
            "Status",
            ["Open", "In Progress", "Resolved", "Closed"],
            index=["Open", "In Progress", "Resolved", "Closed"].index(ticket["Status"])
        )

        new_assignee = st.text_input(
            "Assigned To",
            ticket["Assigned To"]
        )

        if st.button("Update Ticket"):
            tickets.loc[tickets["Ticket ID"] == ticket_id, "Status"] = new_status
            tickets.loc[tickets["Ticket ID"] == ticket_id, "Assigned To"] = new_assignee
            save_tickets(tickets)

            st.success("🔄 Ticket updated successfully!")
