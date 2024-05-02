# ranking-api

## Prepare virual environment in Linux

```cmd
python3 -m  venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Prepare virual environment in Windows

```cmd
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run app

```cmd
streamlit run .\app.py
```

### Secrets

./streamlit/secrets.toml

```toml
url="http://localhost:8000"
```
