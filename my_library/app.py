import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Custom CSS for aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        font-weight: 600;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        background: linear-gradient(45deg, #45a049, #4CAF50);
    }
    
    .book-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #333;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .book-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .book-card:hover::before {
        left: 100%;
    }
    
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .book-card h3 {
        color: #2c3e50;
        margin-bottom: 10px;
        font-weight: 700;
    }
    
    .book-card p {
        margin: 5px 0;
        color: #555;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 3px solid #dee2e6;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        font-weight: 700;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stMetric label {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    .stMetric .metric-value {
        color: #ffffff !important;
        font-size: 2em;
        font-weight: 700;
    }
    
    .stSelectbox, .stTextInput {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
    }
    
    .stSelectbox label, .stTextInput label {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    .genre-badge {
        display: inline-block;
        background: linear-gradient(45deg, #ff6b6b, #ffa500);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px 0;
    }
    
    .due-date {
        color: #e74c3c;
        font-weight: 600;
    }
    
    .success-message {
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .error-message {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = {}
    st.session_state.users = {}
    st.session_state.current_user = None

    # Sample data
    authors = ["J.K. Rowling", "George Orwell", "Jane Austen", "Mark Twain", "Charles Dickens"]
    genres = ["Fiction", "Mystery", "Romance", "Sci-Fi", "Fantasy"]
    for i in range(50):
        book_id = f"B{i+1:03d}"
        title = f"{random.choice(genres)} Adventure {i+1}"
        author = random.choice(authors)
        copies = random.randint(1, 5)
        st.session_state.library[book_id] = {
            'title': title,
            'author': author,
            'total_copies': copies,
            'available_copies': copies,
            'genre': random.choice(genres),
            'image': f"https://picsum.photos/200/300?random={i+1}"
        }

    # Sample users
    st.session_state.users = {
        'admin': {'name': 'Administrator', 'password': 'admin123', 'borrowed': {}, 'fines': 0},
        'user1': {'name': 'Hassan', 'password': 'pass123', 'borrowed': {}, 'fines': 0},
        'user2': {'name': 'Ahmed Raza', 'password': 'pass123', 'borrowed': {}, 'fines': 0},
        'user3': {'name': 'Hamza', 'password': 'pass123', 'borrowed': {}, 'fines': 0},
        'user4': {'name': 'Khabib', 'password': 'pass123', 'borrowed': {}, 'fines': 0},
        'user5': {'name': 'Ali', 'password': 'pass123', 'borrowed': {}, 'fines': 0}
    }

# Helper functions
def borrow_book(book_id, user_id):
    if book_id in st.session_state.library and st.session_state.library[book_id]['available_copies'] > 0:
        if book_id not in st.session_state.users[user_id]['borrowed']:
            st.session_state.library[book_id]['available_copies'] -= 1
            due_date = datetime.now() + timedelta(days=14)
            st.session_state.users[user_id]['borrowed'][book_id] = due_date.strftime("%Y-%m-%d")
            return True
    return False

def return_book(book_id, user_id):
    if book_id in st.session_state.users[user_id]['borrowed']:
        st.session_state.library[book_id]['available_copies'] += 1
        del st.session_state.users[user_id]['borrowed'][book_id]
        return True
    return False

def search_books(query, genre_filter=None):
    results = []
    for book_id, book in st.session_state.library.items():
        if query.lower() in book['title'].lower() or query.lower() in book['author'].lower():
            if genre_filter is None or book['genre'] == genre_filter:
                results.append((book_id, book))
    return results

# App layout
st.title("🌟 📚 Digital Library 📚 🌟")

# Sidebar for user selection and navigation
with st.sidebar:
    if st.session_state.current_user:
        st.header("Navigation")
        menu = st.selectbox("Menu", ["Dashboard", "Browse Books", "My Books", "Add Book"])
        
        st.header(f"Welcome, {st.session_state.users[st.session_state.current_user]['name']}!")
        if st.button("Logout"):
            st.session_state.current_user = None
            st.rerun()
    else:
        st.header("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")
            if login_submitted:
                if username in st.session_state.users and st.session_state.users[username]['password'] == password:
                    st.session_state.current_user = username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.header("Sign Up")
        with st.form("signup_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_name = st.text_input("Full Name")
            signup_submitted = st.form_submit_button("Sign Up")
            if signup_submitted:
                if new_username and new_password and new_name:
                    if new_username not in st.session_state.users:
                        st.session_state.users[new_username] = {
                            'name': new_name,
                            'password': new_password,
                            'borrowed': {},
                            'fines': 0
                        }
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists")
                else:
                    st.error("Please fill all fields")

if st.session_state.current_user:
    current_user_id = st.session_state.current_user

    if menu == "Dashboard":
        st.header("📊 Library Dashboard")
        total_books = len(st.session_state.library)
        total_available = sum(b['available_copies'] for b in st.session_state.library.values())
        total_borrowed = sum(len(u['borrowed']) for u in st.session_state.users.values())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", total_books)
        with col2:
            st.metric("Available Copies", total_available)
        with col3:
            st.metric("Currently Borrowed", total_borrowed)
        
        # Genre distribution pie chart
        genres = {}
        for book in st.session_state.library.values():
            genres[book['genre']] = genres.get(book['genre'], 0) + 1
        genre_df = pd.DataFrame(list(genres.items()), columns=['Genre', 'Count'])
        
        st.subheader("📈 Genre Distribution")
        col4, col5 = st.columns(2)
        with col4:
            st.bar_chart(genre_df.set_index('Genre'))
        with col5:
            import altair as alt
            pie_chart = alt.Chart(genre_df).mark_arc().encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Genre", type="nominal"),
                tooltip=['Genre', 'Count']
            ).properties(width=300, height=300)
            st.altair_chart(pie_chart, use_container_width=True)
        
        # Top authors bar chart
        authors = {}
        for book in st.session_state.library.values():
            authors[book['author']] = authors.get(book['author'], 0) + 1
        top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]
        author_df = pd.DataFrame(top_authors, columns=['Author', 'Books'])
        
        st.subheader("👨‍🎨 Top Authors")
        st.bar_chart(author_df.set_index('Author'))
        
        # Borrowing trends line chart (dummy data)
        import random
        dates = pd.date_range(end=pd.Timestamp.now(), periods=7, freq='D')
        borrowings = [random.randint(0, 10) for _ in range(7)]
        trend_df = pd.DataFrame({'Date': dates, 'Borrowings': borrowings})
        
        st.subheader("📉 Borrowing Trends (Last 7 Days)")
        st.line_chart(trend_df.set_index('Date'))

    elif menu == "Browse Books":
        st.header("🔍 Browse Books")
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search by title or author")
        with col2:
            genre_filter = st.selectbox("Filter by Genre", ["All"] + list(set(b['genre'] for b in st.session_state.library.values())))
        
        genre_filter = None if genre_filter == "All" else genre_filter
        results = search_books(search_query, genre_filter)
        
        if results:
            for book_id, book in results:
                with st.container():
                    st.markdown(f"""
                    <div class="book-card">
                        <img src="{book['image']}" style="width:100px; height:150px; object-fit:cover; border-radius:10px; float:left; margin-right:15px;">
                        <h3>📖 {book['title']}</h3>
                        <p><strong>Author:</strong> ✍️ {book['author']}</p>
                        <span class="genre-badge">{book['genre']}</span>
                        <p><strong>Available:</strong> {book['available_copies']}/{book['total_copies']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Borrow {book_id}", key=f"borrow_{book_id}"):
                        if borrow_book(book_id, current_user_id):
                            st.success(f"Borrowed {book['title']}!")
                            st.rerun()
                        else:
                            st.error("Unable to borrow this book.")
        else:
            st.write("No books found.")

    elif menu == "My Books":
        st.header("📖 My Borrowed Books")
        borrowed = st.session_state.users[current_user_id]['borrowed']
        if borrowed:
            for book_id, due_date in borrowed.items():
                book = st.session_state.library[book_id]
                with st.container():
                    st.markdown(f"""
                    <div class="book-card">
                        <img src="{book['image']}" style="width:100px; height:150px; object-fit:cover; border-radius:10px; float:left; margin-right:15px;">
                        <h3>📖 {book['title']}</h3>
                        <p><strong>Author:</strong> ✍️ {book['author']}</p>
                        <p class="due-date"><strong>Due Date:</strong> 📅 {due_date}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Return {book_id}", key=f"return_{book_id}"):
                        if return_book(book_id, current_user_id):
                            st.success(f"Returned {book['title']}!")
                            st.rerun()
                        else:
                            st.error("Unable to return this book.")
        else:
            st.write("You haven't borrowed any books yet.")

    elif menu == "Add Book":
        st.header("➕ Add New Book")
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            genre = st.selectbox("Genre", ["Fiction", "Mystery", "Romance", "Sci-Fi", "Fantasy", "Other"])
            copies = st.number_input("Number of Copies", min_value=1, value=1)
            image_url = st.text_input("Image URL (optional)", "https://picsum.photos/200/300?random=100")
            submitted = st.form_submit_button("Add Book")
            if submitted:
                book_id = f"B{len(st.session_state.library)+1:03d}"
                st.session_state.library[book_id] = {
                    'title': title,
                    'author': author,
                    'total_copies': copies,
                    'available_copies': copies,
                    'genre': genre,
                    'image': image_url
                }
                st.success(f"Added book: {title}")
                st.rerun()
else:
    st.header("Welcome to Digital Library")
    st.write("Please login or sign up using the sidebar to access the library features.")
    st.markdown("""
    ### Sample Accounts:
    - **admin** / admin123 (Administrator)
    - **user1** / pass123 (hassan)
    - **user2** / pass123 (ahmed raza)
    - And more...
    """)
