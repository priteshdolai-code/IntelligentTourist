# Intelligent Tourist

A travel discovery web application for India. A visitor describes what they want
from a trip in ordinary language, and the app interprets that description,
highlights the matching state on an interactive map of India, and opens a
curated page for that destination.

Built as a team mini-project. The natural-language understanding runs on Azure
Conversational Language Understanding behind a small Flask service.

## How It Works

```
User types a free-text travel description
        ↓
Flask API  (POST /predict_intent)
        ↓
Azure CLU — conversation analysis, returns top intent
        ↓
Intent mapped to ISO state code   e.g. "Goa" → INGA
        ↓
Frontend highlights that state on the SVG map
        ↓
Destination page for that state
```

## Tech Stack

| Layer | Technology |
|---|---|
| NLU | Azure Conversational Language Understanding (CLU) |
| API | Python, Flask, flask-cors |
| Frontend | HTML5, CSS3, JavaScript |
| Map | Interactive SVG map of India, keyed by ISO 3166-2:IN codes |

## Features

- **Natural-language destination matching** — free-text input is classified to a
  destination rather than requiring the user to pick from a dropdown
- **Interactive map of India** — the predicted state is highlighted and links
  through to its page
- **25 destination pages** covering states and union territories
- **Tour customisation** and booking flow pages
- **Photo gallery, blog, about and contact** sections

## Project Structure

```
backend.py           Flask service — CLU intent prediction, state mapping
cover.html           Landing page
startPage.html       Entry point into the app
choice page.html     Trip preference input
customize.html       Itinerary customisation
map.html             Interactive India map
bookTour.html        Booking flow
<state>.html         25 destination pages (goa, kerela, rajasthan, …)
photos/  videos/     Media assets
*.css                Per-page stylesheets
```

## Running Locally

**Prerequisites:** Python 3.9+ and an Azure Language resource with a trained CLU
project.

```bash
git clone https://github.com/priteshdolai-code/IntelligentTourist.git
cd IntelligentTourist

pip install flask flask-cors azure-ai-language-conversations

# Configure credentials (never commit these)
export CLU_ENDPOINT="https://<your-resource>.cognitiveservices.azure.com/"
export CLU_KEY="<your-key>"
export CLU_PROJECT="IntellTour"

python backend.py            # serves on http://localhost:5000
```

Then open `cover.html` in a browser. CORS is enabled on the Flask service so the
static pages can call it directly.

### API

**`POST /predict_intent`**

```json
// request
{ "intent": "I want beaches and nightlife for a long weekend" }

// response
{ "state": "INGA" }
```

## Design Notes

**Why intent classification rather than keyword search.** A keyword matcher
would need an exhaustive synonym list for every state and would still miss
descriptive phrasing like "somewhere cold with mountains." Training a CLU model
on example utterances means the mapping is learned from phrasing rather than
hand-coded, and new example phrasings can be added without touching the code.

**Why map to ISO codes.** The frontend map is an SVG whose regions carry ISO
3166-2:IN identifiers. Translating the model's human-readable intent
("Tamil Nadu") into the map's identifier (`INTN`) at the API boundary keeps the
frontend free of model-specific naming and means a model retrain does not break
the map.

**Why a separate Flask service.** The Azure credentials cannot live in
client-side JavaScript, so the CLU call has to happen server-side. Flask keeps
that boundary thin — one endpoint whose only job is to take text, classify it,
and return a map identifier.

## Known Limitations

- Prediction is limited to the 25 states and union territories present in the
  mapping table.
- Destination pages are static HTML rather than templated from a data source, so
  adding a destination means adding a page.
- The API returns only a state code; entity extraction (duration, budget,
  interests) is not yet wired into the response.
- No automated tests.
- Not deployed — runs locally against a developer Azure resource.

## Credits

Team mini-project, Department of Computer Engineering, VIVA Institute of
Technology.
