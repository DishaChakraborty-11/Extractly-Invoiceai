from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import re

app = Flask(__name__)
CORS(app)

# ── OCR ──────────────────────────────────────────────────────────────
def extract_text_from_image(image_path):
    api_key = os.environ.get("OCR_SPACE_API_KEY", "helloworld")
    url = "https://api.ocr.space/parse/image"

    with open(image_path, "rb") as f:
        response = requests.post(
            url,
            data={
                "apikey": api_key,
                "language": "eng",
                "isOverlayRequired": False,
            },
            files={"file": f},
            timeout=30,
        )

    result = response.json()

    if result.get("OCRExitCode") == 1:
        parsed = result.get("ParsedResults", [])
        if parsed:
            return parsed[0].get("ParsedText", "")
        return ""
    else:
        error_msg = result.get("ErrorMessage", ["Unknown OCR error"])
        raise Exception(f"OCR failed: {error_msg[0] if error_msg else 'Unknown'}")


# ── Parser ────────────────────────────────────────────────────────────
def parse_invoice_fields(text):
    data = {
        "vendor": "Unknown Vendor",
        "date": "Not Found",
        "amount": "Not Found",
    }

    if not text:
        return data

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if lines:
        data["vendor"] = lines[0]

    amount_match = re.search(
        r"(?:total|amount due|amount|due|net|gross|subtotal)[:\s]*\$?\s*([\d,]+\.\d{2})",
        text,
        re.IGNORECASE,
    )
    if amount_match:
        data["amount"] = f"${amount_match.group(1)}"
    else:
        # fallback: find any currency-like number
        fallback = re.search(r"\$\s*([\d,]+\.\d{2})", text)
        if fallback:
            data["amount"] = f"${fallback.group(1)}"

    date_match = re.search(
        r"(\b\d{1,2}[/\.\-]\d{1,2}[/\.\-]\d{2,4}\b)"
        r"|(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b)",
        text,
        re.IGNORECASE,
    )
    if date_match:
        data["date"] = date_match.group(0).strip()

    return data


# ── Routes ────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "InvoiceAI backend is running ✓"})


@app.route("/upload", methods=["POST"])
def upload_invoice():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filepath = os.path.join("/tmp", "invoice_upload.png")
    file.save(filepath)

    try:
        text = extract_text_from_image(filepath)
        fields = parse_invoice_fields(text)
        return jsonify({
            "vendor": fields["vendor"],
            "date": fields["date"],
            "amount": fields["amount"],
            "raw_text": text[:500],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
