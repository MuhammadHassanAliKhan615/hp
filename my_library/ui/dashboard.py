import pandas as pd
import streamlit as st

def show_dashboard(library):
    data = {
        "Title": [],
        "Available": [],
        "Total": []
    }

    for book in library.books.values():
        data["Title"].append(book.title)
        data["Available"].append(book.available_copies)
        data["Total"].append(book.total_copies)

    df = pd.DataFrame(data)

    st.subheader("📊 Library Statistics")
    st.bar_chart(df.set_index("Title")[["Available", "Total"]])

    st.metric("📚 Total Books", len(library.books))
    st.metric("📖 Available Copies", sum(data["Available"]))
