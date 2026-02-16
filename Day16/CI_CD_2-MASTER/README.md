# CI_CD_2-MASTER (Super Calculator)

## Run pipeline
```bash
pip install -r requirements.txt
python pipeline/pipeline.py
```

## What it does
- Installs dependencies
- Runs pytest + unittest
- Copies `app/calculator.py` into `build/`
- Creates `dist/app.zip`
- Copies it to `deploy.zip`

## Monitor (optional)
```bash
python pipeline/monitor.py
```
