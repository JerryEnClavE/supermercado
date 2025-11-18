# My Flask App

This is a basic Flask web application structure.

## Project Structure

```
my-flask-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── templates
│   │   ├── base.html
│   │   └── index.html
│   └── static
│       ├── css
│       │   └── styles.css
│       └── js
│           └── main.js
├── tests
│   └── test_app.py
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-flask-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python run.py
```

Visit `http://127.0.0.1:5000` in your web browser to see the application in action.

## Testing

To run the tests, use:
```
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License.