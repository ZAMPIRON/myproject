# Buddy Matcher

#### Video Demo: 


#### Description:

Buddy Matcher is a web-based application designed to solve a common problem faced by students in online courses like CS50: finding the perfect partner or group for collaborative assignments and final projects. Often, students have great project ideas but lack the specific skills to execute them alone, while others are eager to code but don't have a concrete idea yet. Buddy Matcher bridges this gap by creating a centralized hub where students can connect based on their timezones, GitHub profiles, and project pitches.

The application is built using a full-stack approach, utilizing Python and Flask for the backend server, SQLite for database management, and a mix of HTML, CSS, and vanilla JavaScript for a responsive and dynamic frontend.

### Features & Functionality

At its core, Buddy Matcher requires users to register for an account. During registration, users provide their GitHub username, create a secure password, select their timezone (country), and specify whether they already have a project idea or if they are looking to join someone else's team.

Once logged in, users are greeted by the "Matches" dashboard. This page dynamically pulls registered users from the database and displays them in intuitive, easy-to-read cards. Badges clearly indicate if a user "Has an idea" (highlighted in yellow) or is "Looking to join" (highlighted in blue). From here, users can click to view a detailed Public Profile of any potential buddy, which displays their full project pitch and provides a direct link to their GitHub profile to facilitate contact and collaboration.

### File Structure & Explanations

The project is structured to separate concerns, keeping backend logic, database management, and frontend presentation distinct:

* **`app.py`**: This is the heart of the application. It configures the Flask application, manages user sessions, and defines all the application routes (`/register`, `/login`, `/logout`, `/matches`, and `/user/<account>`). It handles secure password hashing using `werkzeug.security` and executes SQL queries to read and write user data to the SQLite database.
* **`buddy.db`**: The SQLite database file. It contains a `users` table that stores user credentials (hashed passwords), GitHub usernames, country/timezone preferences, their status (idea vs. no idea), and their text pitch.
* **`test_db.py`**: A utility script created to quickly fetch and display the current state of the database directly in the terminal. This was incredibly useful for debugging during development to ensure user data was being inserted correctly.
* **`templates/index.html`**: The base layout file using Jinja templating. It contains the standard HTML boilerplate, links to CSS stylesheets, and the navigation bar. All other HTML files extend this base template to maintain a consistent UI across the app.
* **`templates/register.html` & `templates/login.html**`: The authentication frontend. These contain the HTML forms for user input. They also feature embedded JavaScript that interacts with server-side error messages to trigger visual cues.
* **`templates/matches.html`**: The dashboard template. It uses Jinja `for` loops to iterate over the list of users passed from the backend and generates individual cards for each user.
* **`templates/user.html`**: The public profile template. It displays the specific details of a single user, including a styled blockquote for their project pitch.
* **`static/css/global.css` & `static/css/layout.css**`: These stylesheets define the visual identity of the app. They establish a clean, modern aesthetic utilizing a color palette inspired by academic institutions (featuring Crimson and deep charcoal).

### Design Choices

Throughout the development of Buddy Matcher, several key design choices were made to optimize both the developer experience and the end-user experience:

**1. Vanilla CSS and JavaScript over Heavy Frameworks:**
While frameworks like React or Bootstrap JS components are powerful, I opted to use pure CSS and vanilla JavaScript for the UI elements. For example, instead of relying on standard, static Flask `flash()` messages that permanently take up screen space when a user types a wrong password, I implemented a custom JavaScript and CSS solution. When an authentication error occurs, the error box visually "shakes" using a CSS `@keyframes` animation to grab the user's attention, and a JS `setTimeout` function smoothly fades the error away after 4 seconds. This keeps the interface clean and feels much more premium.

**2. Database Schema and Jinja Integration:**
Initially, SQL queries in the backend used `AS` aliases (e.g., `SELECT country AS timezone`). However, this introduced unnecessary complexity when rendering variables in the Jinja templates, leading to 500 Internal Server Errors when variable names mismatched. The design choice was made to simplify the SQL queries to fetch raw column names (`country`, `pitch`) and update the HTML templates accordingly. This created a more robust, 1:1 mapping between the database schema and the frontend variables, significantly reducing bugs.

**3. Visual Hierarchy using Badges:**
In a list of potential project partners, users need to make quick decisions. I designed the UI to prioritize the "Idea / No Idea" status using distinct colored badges. This design choice prevents users from having to read every single pitch to find what they are looking for, allowing them to visually filter the page in seconds.

Buddy Matcher successfully demonstrates the integration of databases, backend routing, and frontend design, resulting in a practical tool that can help foster collaboration within coding communities.