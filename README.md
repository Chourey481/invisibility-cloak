# Invisibility Cloak 🧙‍♂️

A web application that creates an "invisibility cloak" effect using your webcam. When you cover yourself with a red cloth, the app replaces the red area in the video feed with the previously captured background—making it seem as if you have vanished!

## Features

- Captures background using your webcam.
- Detects red color in real-time and replaces those pixels with background.
- Simple web interface for demonstration.
- Powered by Flask (Python) and OpenCV.

---

## Demo

1. Open the app in your browser.
2. Stand clear so the background can be captured (5 seconds).
3. After confirmation, cover yourself with a red cloth—watch as you become "invisible"!

---

## Installation

### Requirements

- Python 3.9+
- pip
- A webcam

### Clone the repository

```bash
git clone https://github.com/Chourey481/invisibility-cloak.git
cd invisibility-cloak
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Locally

```bash
python app.py
```
The app will be available at http://localhost:8080

### Using Docker

```bash
docker build -t invisibility-cloak .
docker run -p 8080:8080 invisibility-cloak
```

---

## Usage Instructions

1. Navigate to [http://localhost:8080](http://localhost:8080) in your browser.
2. Allow webcam access.
3. Wait 5 seconds for the background capture.
4. After the prompt, hold up a red cloth in front of you—the app will make those areas invisible!

---

## Project Structure

```
invisibility-cloak/
│
├── app.py                # Flask backend with OpenCV processing
├── requirements.txt      # Python dependencies
├── Dockerfile            # Containerization support
├── templates/
│   └── index.html        # Web client UI
└── README.md             # Project documentation
```

---

## How It Works

- The web client captures live video via your webcam.
- After a background snapshot, the server processes each frame:
  - Detects red pixels using HSV color ranges.
  - Replaces red regions with the initial background.
- The result is streamed back to your browser for display.

---

## Troubleshooting

- **Webcam Issues:** Make sure you have allowed browser webcam access.
- **Red Cloth Required:** The effect only works with red color (tuned for a specific red range in HSV).
- **Performance:** Processing happens server-side; CPU performance impacts speed.

---

## License

MIT License

---

## Acknowledgements

Inspired by the classic "Invisibility Cloak" OpenCV project, adapted for web and modern Python.
