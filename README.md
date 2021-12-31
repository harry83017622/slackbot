## **Structure**
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


## **Slack Chatbot Block Format toolkit**
https://api.slack.com/tools/block-kit-builder