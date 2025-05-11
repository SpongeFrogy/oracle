# Trading Solution Frontend

This is the frontend application for the Oracle (Trading Solution) project, built with Streamlit.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/app.py
```

## Features

- User authentication (login/register)
- Secure password handling
- Session management
- Responsive design

## Project Structure

```
frontend/
├── src/
│   ├── app.py        # Main application
│   ├── config.py     # Config application
│   ├── handlers/     # Connection handlers for api
│   └── pages/        # Streamlit pages
└── requirements.txt  # Project dependencies
``` 