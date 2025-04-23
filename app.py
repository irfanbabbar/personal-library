# app.py

import streamlit as st
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚"
)

# File path for storing the library
FILE_PATH = "library.txt"

# Initialize session state variables if they don't exist
if 'library' not in st.session_state:
    # Try to load from file, or start with empty list
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as file:
                st.session_state.library = json.load(file)
                st.success("Library loaded successfully!")
        except:
            st.session_state.library = []
            st.error("Error loading library file. Starting with empty library.")
    else:
        st.session_state.library = []
        st.info("No existing library found. Starting with empty library.")

# Function to save the library to file
def save_library():
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(st.session_state.library, file)
        return True
    except:
        return False

# Main title
st.title("📚 Personal Library Manager")

# Create sidebar menu
st.sidebar.title("Menu")
menu_option = st.sidebar.radio(
    "Choose an option:",
    ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "Exit"]
)

# Add a book
if menu_option == "Add a book":
    st.header("Add a Book")
    
    title = st.text_input("Enter the book title:")
    author = st.text_input("Enter the author:")
    
    # Use a try-except block to handle year input
    year_input = st.text_input("Enter the publication year:", "2000")
    try:
        year = int(year_input)
    except:
        st.error("Please enter a valid year (number).")
        year = 2000
    
    genre = st.text_input("Enter the genre:")
    read_status = st.radio("Have you read this book?", ["yes", "no"])
    
    if st.button("Add Book"):
        if title and author and genre:
            # Create new book dictionary
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read_status == "yes"
            }
            
            # Add to library
            current_library = st.session_state.library
            current_library.append(new_book)
            st.session_state.library = current_library
            
            # Save to file
            if save_library():
                st.success(f"Book '{title}' added successfully!")
            else:
                st.warning("Book added to library but failed to save to file.")
        else:
            st.error("Please fill in all fields.")

# Remove a book
elif menu_option == "Remove a book":
    st.header("Remove a Book")
    
    if not st.session_state.library:
        st.info("Your library is empty.")
    else:
        title_to_remove = st.text_input("Enter the title of the book to remove:")
        
        if st.button("Remove Book"):
            if title_to_remove:
                # Count books before removal
                initial_count = len(st.session_state.library)
                
                # Filter out the book to remove
                updated_library = [book for book in st.session_state.library 
                                  if book["title"].lower() != title_to_remove.lower()]
                
                # Check if any books were removed
                if len(updated_library) < initial_count:
                    st.session_state.library = updated_library
                    
                    # Save to file
                    if save_library():
                        st.success("Book removed successfully!")
                    else:
                        st.warning("Book removed from library but failed to save to file.")
                else:
                    st.error(f"No book with title '{title_to_remove}' found in your library.")
            else:
                st.error("Please enter a title.")

# Search for a book
elif menu_option == "Search for a book":
    st.header("Search for a Book")
    
    if not st.session_state.library:
        st.info("Your library is empty.")
    else:
        search_by = st.radio("Search by:", ["1. Title", "2. Author"])
        
        if search_by == "1. Title":
            search_term = st.text_input("Enter the title:")
            if search_term and st.button("Search"):
                results = [book for book in st.session_state.library 
                          if search_term.lower() in book["title"].lower()]
                
                if results:
                    st.subheader("Matching Books:")
                    for i, book in enumerate(results, 1):
                        read_status = "Read" if book["read"] else "Unread"
                        st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
                else:
                    st.info(f"No books found matching '{search_term}'.")
        else:  # Author
            search_term = st.text_input("Enter the author:")
            if search_term and st.button("Search"):
                results = [book for book in st.session_state.library 
                          if search_term.lower() in book["author"].lower()]
                
                if results:
                    st.subheader("Matching Books:")
                    for i, book in enumerate(results, 1):
                        read_status = "Read" if book["read"] else "Unread"
                        st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
                else:
                    st.info(f"No books found matching '{search_term}'.")

# Display all books
elif menu_option == "Display all books":
    st.header("Your Library")
    
    if not st.session_state.library:
        st.info("Your library is empty.")
    else:
        st.subheader("All Books:")
        for i, book in enumerate(st.session_state.library, 1):
            read_status = "Read" if book["read"] else "Unread"
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

# Display statistics
elif menu_option == "Display statistics":
    st.header("Library Statistics")
    
    if not st.session_state.library:
        st.info("Your library is empty.")
    else:
        total_books = len(st.session_state.library)
        read_books = sum(1 for book in st.session_state.library if book["read"])
        
        if total_books > 0:
            percentage_read = (read_books / total_books) * 100
        else:
            percentage_read = 0
        
        st.write(f"Total books: {total_books}")
        st.write(f"Percentage read: {percentage_read:.1f}%")

# Exit (save and exit)
elif menu_option == "Exit":
    st.header("Exit")
    
    if st.button("Save and Exit"):
        if save_library():
            st.success("Library saved to file. Goodbye!")
        else:
            st.error("Failed to save library.")

# Always show a save button at the bottom of the sidebar
if st.sidebar.button("Save Library"):
    if save_library():
        st.sidebar.success("Library saved successfully!")
    else:
        st.sidebar.error("Failed to save library.")

# Display current library status
st.sidebar.write(f"Current library: {len(st.session_state.library)} books")