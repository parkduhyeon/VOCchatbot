#!/bin/bash
python3 -m pip install --upgrade pip
python3 -m pip install -r /home/site/wwwroot/requirements.txt
exec python3 -m streamlit run /home/site/wwwroot/app.py --server.port 8000 --server.address 0.0.0.0
