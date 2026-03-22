# intent-and-entities-extraction-SaraSopr

## Project initialization

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create your local environment file:

```bash
cp .env.example .env
```

4. Start Jupyter and open `excercise.ipynb`:

```bash
jupyter notebook
```

## Dataset usage

You can use either:

- A local dataset file in `data/raw/` (supported: `.csv`, `.json`, `.jsonl`, `.parquet`)
- A Hugging Face dataset ID (default in `.env.example`)

Set one of these in `.env`:

- `LOCAL_DATASET_PATH=data/raw/your_dataset.csv`
- or `HF_DATASET_ID=owner/dataset_name` and `HF_DATASET_SPLIT=train`

The notebook is configured to:

1. Read settings from `.env`
2. Load local file if `LOCAL_DATASET_PATH` is set
3. Otherwise load the Hugging Face dataset
4. Show dataset shape and sample rows for quick validation
