from pydantic import BaseModel, Field


class StructureCalcRequest(BaseModel):
    span_m: float = Field(gt=0, description="Beam span, m")
    load_kn_m: float = Field(gt=0, description="Uniform load, kN/m")


class StructureCalcResponse(BaseModel):
    moment_kn_m: float = Field(description="Maximum bending moment, kN·m")


class MixPropertiesRequest(BaseModel):
    cement_kg_m3: float = Field(gt=0, description="Cement content, kg/m³")
    water_kg_m3: float = Field(gt=0, description="Water content, kg/m³")


class MixPropertiesResponse(BaseModel):
    water_cement_ratio: float = Field(description="w/c ratio, dimensionless")


class LifetimePredictionRequest(BaseModel):
    cover_mm: float = Field(gt=0, description="Concrete cover thickness, mm")
    chloride_exposure_factor: float = Field(gt=0, description="Exposure factor")


class LifetimePredictionResponse(BaseModel):
    predicted_years: float = Field(description="Predicted service life, years")


class CompareRequest(BaseModel):
    left_value: float
    right_value: float


class CompareResponse(BaseModel):
    difference: float
    winner: str
