from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"


# Connect Flask to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Siya@2007",
        database="notes_db"
    )


# Display all notes
@app.route("/")
def index():
    search = request.args.get("search", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if search:
            sql = """
                SELECT * FROM notes
                WHERE title LIKE %s OR content LIKE %s
                ORDER BY id DESC
            """
            value = "%" + search + "%"
            cursor.execute(sql, (value, value))
        else:
            cursor.execute("SELECT * FROM notes ORDER BY id DESC")

        notes = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template(
        "index.html",
        notes=notes,
        search=search
    )



# Add a new note
@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("Please enter both a title and content.", "error")
        return redirect(url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (%s, %s)",
            (title, content)
        )
        conn.commit()
        flash("Note added successfully!", "success")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("index"))


# Edit an existing note
@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()

            if not title or not content:
                flash("Title and content cannot be empty.", "error")
            else:
                cursor.execute(
                    "UPDATE notes SET title = %s, content = %s WHERE id = %s",
                    (title, content, note_id)
                )
                conn.commit()

                if cursor.rowcount:
                    flash("Note updated successfully!", "success")
                else:
                    flash("No changes were made, or note was not found.", "error")

                return redirect(url_for("index"))

        cursor.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
        note = cursor.fetchone()

        if note is None:
            flash("Note not found.", "error")
            return redirect(url_for("index"))

        return render_template("edit.html", note=note)

    finally:
        cursor.close()
        conn.close()


# Delete a note
@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        conn.commit()

        if cursor.rowcount:
            flash("Note deleted successfully!", "success")
        else:
            flash("Note not found.", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
