from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class Project(ProjectBase):
    id: int


class VariantBase(BaseModel):
    project_id: int
    name: str


class Variant(VariantBase):
    id: int


class MaterialBase(BaseModel):
    name: str
    density_kg_m3: float = Field(description="Density, kg/m³")


class Material(MaterialBase):
    id: int


class MixBase(BaseModel):
    project_id: int
    water_cement_ratio: float = Field(description="w/c ratio, dimensionless")


class Mix(MixBase):
    id: int


class CalculationBase(BaseModel):
    variant_id: int
    load_kn: float = Field(description="Design load, kN")


class Calculation(CalculationBase):
    id: int


class ReportBase(BaseModel):
    project_id: int
    title: str


class Report(ReportBase):
    id: int
