import io
import joblib
import pandas as pd 
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI()

model = joblib.load("house_model.joblib")
features = joblib.load("house_features.joblib")

#input schema
class HouseFeatures(BaseModel):
    MedInc:     float = Field(gt = 0 , description="Median income of neighborhood")
    HouseAge:   float = Field(gt = 0, description="Median house age in neighborhood")
    AveRooms:   float = Field(gt = 0, description="Average number of rooms per household")
    AveBedrms:  float = Field(gt = 0, description="Average number of bedrooms per household")
    Population: float = Field(gt = 0, description="Population of neighborhood")
    AveOccup:   float = Field(gt = 0, description="Average number of household members")  
    Latitude:   float = Field(ge = -90, le = 90, description="Latitude of neighborhood")
    Longitude:  float = Field(ge = -180, le = 180, description="Longitude of neighborhood")
    
#home
@app.get("/")
def home():
    return {"message": "Welcome to the California housing price prediction API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": "send POST request to /predict with house features to get price prediction"
            }

@app.get("/health")
def health():
    return {"status": "healthy",
            "model": "RandomForestRegressor",
            "features": features,
            "avg_error": "32754.0 USD",
            }
    
#prediction endpoint
@app.post("/predict")
def predict(house: HouseFeatures):
    try:
        input_data = pd.DataFrame([{
            "MedInc": house.MedInc,
            "HouseAge": house.HouseAge,
            "AveRooms": house.AveRooms,
            "AveBedrms": house.AveBedrms,
            "Population": house.Population,
            "AveOccup": house.AveOccup,
            "Latitude": house.Latitude,
            "Longitude": house.Longitude
        }])
        
        prediction = model.predict(input_data)[0]
        price_usd = prediction * 100000
        return {"predicted_price": f"${price_usd:,.0f}",
                "predicted_price_short": f"${prediction:,.2f} hundred thousand",
                "confidence_range": f"${price_usd - 32754:,.0f} - ${price_usd + 32754:,.0f}"}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")   
    

# uvicorn main:app --reload

@app.post("/predict_file")
async def predict_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    required_columns = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing_columns)}")
    
    if len(df) == 0:
        raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")
    
    try: 
        predictions = model.predict(df[required_columns])
        df['predicted_price_usd'] = predictions * 100000
        df['predicted_price_usd'] = df['predicted_price_usd'].apply(lambda x: f"${x:,.0f}")
        
        output = df.to_csv(index=False)
        
        return StreamingResponse(io.StringIO(output), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=predictions.csv"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
    
    