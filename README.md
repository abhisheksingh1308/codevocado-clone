# Codevocado 🥑

Codevocado is a secure online assessment platform designed for educators and students. It provides a modern, responsive interface for managing exams, tracking progress, and delivering secure tests.

![Codevocado Hero](static/logo.png)

## 🚀 Features

*   **Responsive Design**: Fully optimized for Mobile, Tablet, and Desktop devices.
*   **User Dashboard**: Manage assessments, view history, and create new tests.
*   **Assessment Creation**: Dynamic form builder for creating questions with multiple-choice options.
*   **Secure Authentication**: Login system with session management.
*   **Modern UI/UX**:
    *   Animated interactions (Float, FadeInUp).
    *   Glassmorphism effects.
    *   Interactive mobile navigation.
    *   Dark mode compatible structure.

## 🛠️ Tech Stack

*   **Backend**: Python (Flask)
*   **Database**: MySQL
*   **Frontend**: HTML5, CSS3 (Flexbox/Grid), JavaScript (ES6+)

## ⚙️ Installation & Setup

### Prerequisites

*   Python 3.x
*   MySQL Server installed and running

### Steps

1.  **Clone the repository** (or extract the project files):
    ```bash
    cd codevocado
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Configuration**:
    Open `app.py` and update the `db_config` dictionary with your MySQL credentials:
    ```python
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'mysqlvivo',  # <--- Update this
        'database': 'codevocado_db'
    }
    ```

4.  **Run the Application**:
    ```bash
    python app.py
    ```
    The application will automatically create the database and necessary tables on the first run.

5.  **Access the App**:
    Open your browser and navigate to: `http://127.0.0.1:5000`

## 🔑 Demo Access (For Humans)

We've set up a default account so you can jump right in and test the features without hassle.

*   **Username**: `admin`
*   **Password**: `password123`

> **Note**: These credentials are automatically generated when you run the app for the first time. You can use them to log in and access the dashboard.

## 📂 Project Structure

```
codevocado/
├── static/
│   ├── style.css       # Main stylesheet (Responsive & Animations)
│   ├── script.js       # Frontend logic (Modals, Mobile Menu)
│   └── logo.png        # Project assets
├── templates/
│   ├── index.html      # Landing page
│   ├── login.html      # Authentication page
│   └── dashboard.html  # User dashboard
├── app.py              # Flask application & DB logic
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🎨 UI Highlights

*   **Hero Section**: Features a floating logo animation and staggered text entry.
*   **Footer**: Includes a polished, app-icon style brand mark with hover lift effects.
*   **Mobile Menu**: Smooth slide-down hamburger menu for smaller screens.

## 📄 License

This project is for educational purposes.
