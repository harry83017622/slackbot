## **Usage**
```
conda create --name slackbot python=3.8
conda activate slackbot
pip install -e ".[develop]"

// Acquire the same data from gcp bucket, prepare this for daily ranking in slack.
make -f Makefile write_record_to_local

// upload db to gcp bucket, this action needs credential.
make -f Makefile upload_record
```

For daily slack posting, please read comment in main.py

## **Structure**
```
.
│  .gitignore
│  config.json          // Secret token
│  main.py              // Entry point
│  README.md
│  requirements.txt
│
├─control
│  │  control.py        // Handle task logic
│
├─model
│  │  auth.py
│  │  model.py          // Handle db query
│
├─view
│  │  template.py
│  │  view.py           // Handle slack msg
```

## **Slack Chatbot Block Format toolkit**
https://api.slack.com/tools/block-kit-builder