# AI Data Collector

This is a minimal example of an AI-powered data collector. It provides a Flask backend that accepts free-form text, extracts simple numeric features from it, and stores the result in `data/dataset.json`. The front-end is a basic HTML page that lets you submit new entries.

## Requirements

- Python 3.11
- Flask
- pandas

## Running

Install dependencies and start the server:

```bash
pip install flask pandas
python -m backend.app
```

Open a browser at [http://localhost:5000](http://localhost:5000) to add new text entries. Collected data can be found in `data/dataset.json`.

## OpenAI Configuration

If you use the optional `plugins.model` helper, it can automatically detect
an API key from the `OPENAI_API_KEY` environment variable when one is not
explicitly provided. You may also use `env:VAR_NAME` notation to reference
other environment variables when calling `connect`.
