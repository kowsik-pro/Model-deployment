from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated
import pickle
import pandas as pd



with open("laptop_price_model.pkl", "rb") as f:
    model = pickle.load(f)


app = FastAPI(
    title="Laptop Price Prediction API",
    description=" To predict laptop prices",
    version="1.0"
)



class Laptop(BaseModel):

    Company: Annotated[str,Field(...,description="Laptop manufacturer",examples=["Dell", "HP", "Lenovo"])]

    TypeName: Annotated[str,Field(...,description="Type of laptop",examples=["Notebook", "Ultrabook", "Gaming"])]

    Inches: Annotated[float,Field(...,gt=0,lt=30,description="Screen size in inches",examples=[13.3, 15.6])]

    Ram: Annotated[int,Field(...,gt=0,description="RAM in GB",examples=[8, 16, 32])]

    OpSys: Annotated[str,Field(...,description="Operating system",examples=["Windows 10", "macOS", "Linux"])]

    Weight: Annotated[float,Field(...,gt=0,description="Laptop weight in kilograms",examples=[1.37, 2.0] )]

    ScreenWidth: Annotated[int,Field(...,gt=0,description="Screen width in pixels",examples=[1920, 2560])]

    ScreenHeight: Annotated[int,Field(...,gt=0,description="Screen height in pixels",examples=[1080, 1600])]

    IPS: Annotated[int,Field(...,ge=0,le=1,description="Whether the display has an IPS panel (0 or 1)",examples=[0, 1])]

    CpuBrand: Annotated[str,Field(..., description="CPU manufacturer", examples=["Intel", "AMD"] )]

    CpuSpeed: Annotated[float,Field(...,gt=0,description="CPU speed in GHz",examples=[2.3, 3.2])]

    SSD_GB: Annotated[float,Field(...,ge=0,description="SSD storage in GB",examples=[256, 512])]

    HDD_GB: Annotated[float,Field(...,ge=0,description="HDD storage in GB",examples=[0, 1024])]

    Hybrid_GB: Annotated[float,Field(...,ge=0,description="Hybrid storage in GB",examples=[0, 1024])]
   

    Flash_GB: Annotated[float,Field(...,ge=0,description="Flash storage in GB",examples=[0, 32])]

    GpuBrand: Annotated[str,Field(...,description="GPU manufacturer",examples=["Intel", "Nvidia", "AMD"] )]



    @computed_field
    @property
    def total_storage(self) -> float:
        return (self.SSD_GB + self.HDD_GB + self.Hybrid_GB+ self.Flash_GB)

 

    @field_validator("Company", "CpuBrand", "GpuBrand", "OpSys", "TypeName")
    @classmethod
    def remove_extra_spaces(cls, value):
        return value.strip()




@app.get("/")
def home():
    return {
        "message": "Laptop Price Prediction  is running"
    }



@app.post("/predict")
def predict_price(laptop: Laptop):

    data = laptop.model_dump(exclude={"total_storage"})

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)

    return {
        "message": "Prediction successful",
        "predicted_price": round(float(prediction[0]), 2)
    }