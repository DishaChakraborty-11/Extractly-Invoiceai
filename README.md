# Extractly — AI Invoice Expense Tracker 🧾

> Upload any invoice or receipt. AI extracts vendor, date & amount instantly.

**Live Backend:** [extractly-invoiceai.onrender.com](https://extractly-invoiceai.onrender.com)

---

## What it does

Extractly is an AI-powered invoice scanner that reads any invoice image (PNG, JPG, PDF) and automatically extracts:

- **Vendor name** — who issued the invoice
- **Date** — when it was issued
- **Amount** — total due
- **Session summary** — tracks total spend and unique vendors across multiple scans

No manual entry. Just upload and go.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML / CSS / JS |
| Backend | Flask (Python) |
| OCR Engine | OCR.space API |
| Hosting | Render (backend) + GitHub Pages (frontend) |

---

## How it works

1. User uploads an invoice image via the frontend
2. Flask backend receives the file and sends it to OCR.space API
3. OCR.space extracts raw text from the image
4. A regex parser detects vendor, date, and amount fields
5. Results are returned to the frontend and displayed instantly

---

## Running locally

**Backend**

```bash
git clone https://github.com/DishaChakraborty-11/Extractly-Invoiceai
cd Extractly-Invoiceai
pip install -r requirements.txt
export OCR_SPACE_API_KEY=your_key_here
python app.py
```

Backend runs at `http://localhost:5000`

**Frontend**

Open `index.html` in your browser. Set the Backend URL field to `http://localhost:5000`.

---

## Environment Variables

| Variable | Description |
|---|---|
| `OCR_SPACE_API_KEY` | Free API key from [ocr.space](https://ocr.space/ocrapi) |

---

## Project Structure

```
Extractly-Invoiceai/
├── app.py            # Flask backend + OCR + parser
├── requirements.txt  # Python dependencies
├── index.html        # Frontend (standalone, no build step)
└── README.md
```

---
## Screenshots
<img width="1920" height="868" alt="Screenshot (57)" src="https://github.com/user-attachments/assets/8f5f3be9-1e94-4c99-82b7-8f6fdbdfe0d4" />
<img width="1895" height="859" alt="Screenshot (58)" src="https://github.com/user-attachments/assets/064a1192-431e-48e4-9a93-acef2ace1749" />
<img width="1906" height="871" alt="Screenshot (59)" src="https://github.com/user-attachments/assets/91e63f0e-7184-493a-b9e2-e06dcb18d7c2" />


## Features

- Drag & drop or click to upload invoices
- Supports PNG, JPG, PDF formats
- Session history table with all scanned invoices
- Running total of detected amounts
- Unique vendor count tracker
- Raw OCR text preview toggle
- Configurable backend URL (works with any host)

---

## Limitations

- OCR accuracy depends on invoice image quality
- Free OCR.space tier has a monthly limit of 500 requests
- Parser uses regex — complex or unusual invoice layouts may not parse perfectly

---

## Previous Version

An earlier iteration using Tesseract OCR + spaCy + SQLite is available at [invoice-ai-expense-tracker](https://github.com/DishaChakraborty-11/invoice-ai-expense-tracker).

---

## License

MIT © Disha Chakraborty
