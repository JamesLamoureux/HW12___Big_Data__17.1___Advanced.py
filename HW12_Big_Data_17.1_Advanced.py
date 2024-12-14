import sqlite3

# Initialize the database (Run this part once)
with open('books.sql', 'r') as sql_file:
    sql_script = sql_file.read()

connection = sqlite3.connect("books.db")
cursor = connection.cursor()
cursor.executescript(sql_script)
connection.commit()
print("Database initialized successfully.")

# Task Execution
try:
    # Task 1: Select all authors’ last names in descending order
    cursor.execute("SELECT last FROM authors ORDER BY last DESC;")
    authors_last_names = cursor.fetchall()
    print("Authors' Last Names (Descending Order):")
    for last_name in authors_last_names:
        print(last_name[0])

    # Task 2: Select all book titles in ascending order
    cursor.execute("SELECT title FROM titles ORDER BY title ASC;")
    book_titles = cursor.fetchall()
    print("\nBook Titles (Ascending Order):")
    for title in book_titles:
        print(title[0])

    # Task 3: Use an INNER JOIN to select all the books for a specific author
    # Include the title, copyright year, and ISBN, ordered alphabetically by title
    specific_author = 'Deitel'  # Replace with the desired author's last name
    cursor.execute(
        """
        SELECT titles.title, titles.copyright, titles.isbn 
        FROM titles
        INNER JOIN author_ISBN ON titles.isbn = author_ISBN.isbn
        INNER JOIN authors ON author_ISBN.id = authors.id
        WHERE authors.last = ?
        ORDER BY titles.title ASC;
        """, (specific_author,))
    author_books = cursor.fetchall()
    print(f"\nBooks by {specific_author} (Ordered by Title):")
    for book in author_books:
        print(f"Title: {book[0]}, Copyright: {book[1]}, ISBN: {book[2]}")

    # Task 4: Insert a new author into the authors table
    new_author = ('Grace', 'Hopper')
    cursor.execute("INSERT INTO authors (first, last) VALUES (?, ?);", new_author)
    connection.commit()
    print("\nNew author inserted successfully.")
    
    try:
        new_author = ('Grace', 'Hopper')
        cursor.execute("INSERT INTO authors (first, last) VALUES (?, ?);", new_author)
        connection.commit()
        print("\nNew author inserted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    # Task 5: Insert a new title for an author
    new_title = ('9780134685991', 'Introduction to Computing', 1, '2024')  # isbn, title, edition, copyright
    cursor.execute("INSERT INTO titles (isbn, title, edition, copyright) VALUES (?, ?, ?, ?);", new_title)
    connection.commit()
    print("\nNew title inserted successfully.")

    # Link the new book to the new author
    cursor.execute("SELECT id FROM authors WHERE last = ? AND first = ?;", new_author)
    author_row = cursor.fetchone()

    if author_row is None:
        print(f"\nError: No author found with name {new_author[1]}, {new_author[0]}.")
    else:
        author_id = author_row[0]
        cursor.execute("INSERT INTO author_ISBN (id, isbn) VALUES (?, ?);", (author_id, new_title[0]))
        connection.commit()
        print("\nNew title and author_ISBN entry inserted successfully.")


except sqlite3.Error as e:
        print("An error occurred:", e)
finally:
        # Close the connection
   connection.close()
   

