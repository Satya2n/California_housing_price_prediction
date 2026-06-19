# California Housing Price Prediction API

This project is a FastAPI application that predicts California house prices using a trained machine learning model. The API accepts housing features, sends them to the saved model, and returns an estimated house price.

The project shows a simple end-to-end machine learning deployment flow: prepare a model, save it, load it inside an API, and expose prediction endpoints for users.

## Project Objective

The main objective is to reduce manual price estimation and make predictions:

- Faster
- More consistent
- Easier to use through an API
- Available locally through a web server

## Project Files

```text
project_1/
|-- main.py                         # FastAPI application
|-- README.md                       # Project documentation
|-- fetch_california_housing.xlsx   # Dataset used for the project
|-- house_model.joblib              # Saved trained model
|-- house_features.joblib           # Saved model feature names
|-- test_houses.csv                 # Sample CSV file for batch prediction
|-- explore.ipynb                   # Notebook for data exploration/training work
|-- text.md                         # Rough project notes
`-- __pycache__/                    # Python cache folder
```

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
- Joblib
- Pydantic

## How The Project Works

1. The trained machine learning model is saved in `house_model.joblib`.
2. The model feature names are saved in `house_features.joblib`.
3. `main.py` loads both files when the API starts.
4. The user sends housing feature values to the API.
5. The API converts the input into a Pandas DataFrame.
6. The model predicts the house price.
7. The API returns the prediction as a JSON response or downloadable CSV file.

## Model Input Features

| Feature | Description |
|---|---|
| MedInc | Median income in the neighborhood |
| HouseAge | Median house age in the neighborhood |
| AveRooms | Average number of rooms per household |
| AveBedrms | Average number of bedrooms per household |
| Population | Population of the neighborhood |
| AveOccup | Average number of household members |
| Latitude | Latitude of the neighborhood |
| Longitude | Longitude of the neighborhood |

## API Endpoints

### Home

```http
GET /
```

Returns a welcome message, API version, status, and basic endpoint information.

### Health Check

```http
GET /health
```

Returns API health information, model name, feature list, and average error.

### Predict One House Price

```http
POST /predict
```

Accepts one house record as JSON and returns the predicted price.

Example request body:

```json
{
  "MedInc": 8.3,
  "HouseAge": 30,
  "AveRooms": 6.5,
  "AveBedrms": 1.02,
  "Population": 340,
  "AveOccup": 2.55,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

Example response:

```json
{
  "predicted_price": "$452,600",
  "predicted_price_short": "$4.53 hundred thousand",
  "confidence_range": "$419,846 - $485,354"
}
```

### Predict Prices From CSV

```http
POST /predict_file
```

Accepts a `.csv` file and returns a downloadable CSV file with a new `predicted_price_usd` column.

The CSV file must contain these columns:

```text
MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude
```

You can use `test_houses.csv` as a sample input file.

## How To Run Locally

Open PowerShell and move into the project folder:

```powershell
cd C:\Local_my_projects\my_projects\Docs_my_projects\project_1
```

Activate the virtual environment:

```powershell
..\..\my_venv\Scripts\Activate.ps1
```

Install dependencies if they are not already installed:

```powershell
pip install fastapi uvicorn pandas scikit-learn joblib python-multipart openpyxl
```

Run the API:

```powershell
uvicorn main:app --reload
```

Open the API in your browser:

```text
http://127.0.0.1:8000
```

Open the automatic FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing The API

After starting the server, go to:

```text
http://127.0.0.1:8000/docs
```

Then test:

1. `GET /` to check the home route.
2. `GET /health` to check model and API status.
3. `POST /predict` to predict one house price using JSON input.
4. `POST /predict_file` to upload `test_houses.csv` and download predictions.

## Important Notes

Run the server from inside the `project_1` folder. The API loads `house_model.joblib` and `house_features.joblib` using relative paths, so running the command from another folder may cause file loading errors.

Correct command:

```powershell
uvicorn main:app --reload
```

Incorrect command:

```powershell
uvivorn main:app --reload
```

## Summary

This project converts a machine learning house price prediction model into a local API. It is useful for learning how to connect machine learning models with FastAPI and serve predictions through HTTP endpoints.
