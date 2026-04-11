# LOCAL RUNBOOK

## Install
```bash
python -m pip install --upgrade pip
pip install -e . pytest
```

## List workflows
```bash
python titanius_cli.py list
```

## Run the first workflow
```bash
python titanius_cli.py run lead_recovery_audit --input samples/leads_demo.v1.json --mode report --output-json reports/lead_recovery.json --output-md reports/lead_recovery.md
```

## Dry run
```bash
python titanius_cli.py run lead_recovery_audit --input samples/leads_demo.v1.json --mode dry
```

## Run tests
```bash
pytest -q
```

## What success looks like
- the CLI prints a JSON envelope
- `reports/lead_recovery.json` is created
- `reports/lead_recovery.md` is created
- tests pass

## First debugging checks
- verify Python 3.11+
- verify the input path exists
- verify the JSON file contains a list of records
- verify `estimated_value`, `reply_count`, and `meeting_count` are numeric-like where possible
