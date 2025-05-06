# **SocialSpy**

**SocialSpy** is a social media profile web scraping application. It supports:

- 🖥️ **Desktop Application** (Custom Tkinter-based UI)
- 🌐 **Web-based Flask App**
- 💻 **Direct JavaScript Version**

---

## 🚀 **Getting Started**

### 🖥️ **Run Desktop Application (Python GUI)**

To launch the desktop GUI with a basic Instagram scraping demo:

```bash
cd path/to/Desktop Application Python 
python Main.py
```

---

### 🌐 **Run Flask Web Version**

To start the web-based Flask app:

```bash
cd path/to/Web UI Part Flask
python app.py
```

Open the browser and go to the URL shown in your terminal (e.g., `http://127.0.0.1:5000`).

---

### 💻 **Run Direct JS Version**

1. Go to the `Web Ui Basic html,css,js` folder.
2. Open `index.html` in your browser.

> ⚠️ **Make sure your browser allows local JavaScript execution.**

---

## 📁 **Project Structure**

```
SocialSpy/
├── Desktop Application Python /         # desktop GUI
├── Web UI Part Flask/       # Flask web interface
├── Web Ui Basic html,css,js/          # Direct HTML + JS implementation
└── scp/                 # Common scraping scripts and utilities
```

---

## ⚙️ **Scripts and Utilities**

All core scraping functionality is housed in the `scp/` folder. These modules are shared and reused by the Flask and JS versions.

---

## ✅ **Usage Notes**

- For **desktop GUI**, run `main.py` inside `desktop-app`.
- For **Flask app**, run `app.py` from the root of the respective folder.
- For **JS version**, open the HTML file in your browser.
- Make sure required dependencies (Flask, etc.) are installed.

---

Install dependencies correctly first

---

## 📜 **License**

This project is licensed under the MIT License.
