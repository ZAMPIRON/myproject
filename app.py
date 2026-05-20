from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db, init_db, close_db

app = Flask(__name__)
app.secret_key = "cs50"  # I set this secret key because Flask needs it to manage sessions

with app.app_context():
    init_db()

app.teardown_appcontext(close_db)

@app.get("/")
def index():
    return redirect("/matches") if session.get("user_id") else render_template("index.html")

# REGISTER
@app.get("/register")
def register_view():
    return render_template("register.html")

@app.post("/register")

def register_action():
    account = request.form.get("account", "").strip()
    password = request.form.get("password")
    country = request.form.get("country")
    
    db = get_db()
    # I used a SELECT query here to check if the username is already taken
    if db.execute("SELECT id FROM users WHERE account = ?", (account,)).fetchone(): 
        # If the username is already taken, I show this error message
        return render_template("register.html", error="Username already registered.") 
        
    # I used an INSERT command here to add the new user with their country into the database
    db.execute("INSERT INTO users (account, hash, country, has_idea) VALUES (?, ?, ?, ?)", 
               (account, generate_password_hash(password), country, request.form.get("has_idea", "no"))) # I hashed the password for security and set has_idea to 'no' by default
    db.commit() # I committed the changes to save them into the database
    return redirect("/login") # After registering, I redirect the user to the login page

# LOGIN and LOGOUT 
@app.get("/login")
def login_view():
    session.clear()
    return render_template("login.html")

@app.post("/login")
def login_action():
    account = request.form.get("account", "").strip()
    password = request.form.get("password")
    # I checked if the user exists using a SELECT query
    user = get_db().execute("SELECT * FROM users WHERE account = ?", (account,)).fetchone() 
    
    # I verified if the user actually exists and if the password matches the hash
    if user and check_password_hash(user["hash"], password): 
        session["user_id"] = user["id"] # I set the session id to the user's id to keep them logged in
        return redirect("/matches")
        
    return render_template("login.html", error="Invalid username or password.")

@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")

# Profile
@app.get("/profile")
def profile_view():
    if "user_id" not in session: return redirect("/login")
    user = get_db().execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("profile.html", user=user)

# I created this route to update the user's profile information in the database
@app.post("/profile") 
def profile_action():
    if "user_id" not in session: return redirect("/login")
    db = get_db()
    # I used an UPDATE query to save the user's new country and idea status
    db.execute("UPDATE users SET country = ?, has_idea = ? WHERE id = ?", 
               (request.form.get("country"), request.form.get("has_idea", "no"), session["user_id"]))
    db.commit()
    return redirect("/profile")

# PITCH
@app.get("/pitch")
def pitch_view():
    if "user_id" not in session: return redirect("/login")
    user = get_db().execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("pitch.html", user=user)

@app.post("/pitch")
def pitch_action():
    if "user_id" not in session: return redirect("/login")
    # if the user wants to delete the pitch I set the text to an empty string, otherwise I get it from the form
    text = "" if request.form.get("action") == "delete" else request.form.get("text", "").strip() 
    db = get_db()
    db.execute("UPDATE users SET pitch = ? WHERE id = ?", (text, session["user_id"])) # I updated the pitch text here
    db.commit()
    return redirect("/pitch")

# Filter and Search
@app.get("/matches")
def matches():
    if "user_id" not in session: return redirect("/login")
    
    db = get_db()
    # I fetched the filter parameters directly from the query string
    filter_country = request.args.get("country", "")
    filter_idea = request.args.get("idea", "")

    query = "SELECT * FROM users WHERE id != ?" 
    params = [session["user_id"]]
    
    # If a country filter was selected, I added it to my dynamic query and parameters list
    if filter_country: query += " AND country = ?"; params.append(filter_country) 
    # If an idea filter was selected, I appended it just like I did with the country
    if filter_idea: query += " AND has_idea = ?"; params.append(filter_idea) 
    
    users = db.execute(query + " ORDER BY account", params).fetchall() # I sorted the resulting users by their account name
    # I fetched all users except the current one to dynamically populate my country filter dropdown
    all_users = db.execute("SELECT country FROM users WHERE id != ?", (session["user_id"],)).fetchall() 
    
    countries = sorted(set(u["country"] for u in all_users if u["country"])) # I filtered unique countries for the dropdown options
    
    return render_template("matches.html", users=users, countries=countries,
                           filter_country=filter_country, filter_idea=filter_idea)

# --- PUBLIC PROFILE ---
@app.get("/user/<account>")
def view_user(account):
    if "user_id" not in session: return redirect("/login")
    user = get_db().execute("SELECT * FROM users WHERE account = ?", (account,)).fetchone()
    return redirect("/matches") if not user else render_template("user.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)