# Flask Web Application

This is a simple Flask web application that demonstrates the basic structure and functionality of a Flask project.

## Project Structure

```
flask-web-app
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
│       │   └── style.css
│       └── js
│           └── main.js
├── tests
│   └── test_app.py
├── requirements.txt
├── config.py
├── run.py
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd flask-web-app
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python run.py
```
The application will be accessible at `http://127.0.0.1:5000`.

## Testing

To run the tests, use:
```
pytest tests/test_app.py
```

## License

This project is licensed under the MIT License.