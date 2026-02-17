from app.repositories.base import InMemoryRepository
from app.schemas.resources import (
    Calculation,
    CalculationBase,
    Material,
    MaterialBase,
    Mix,
    MixBase,
    Project,
    ProjectBase,
    Report,
    ReportBase,
    Variant,
    VariantBase,
)

project_repo = InMemoryRepository[ProjectBase, Project](lambda i, p: Project(id=i, **p.model_dump()))
variant_repo = InMemoryRepository[VariantBase, Variant](lambda i, p: Variant(id=i, **p.model_dump()))
material_repo = InMemoryRepository[MaterialBase, Material](lambda i, p: Material(id=i, **p.model_dump()))
mix_repo = InMemoryRepository[MixBase, Mix](lambda i, p: Mix(id=i, **p.model_dump()))
calculation_repo = InMemoryRepository[CalculationBase, Calculation](
    lambda i, p: Calculation(id=i, **p.model_dump())
)
report_repo = InMemoryRepository[ReportBase, Report](lambda i, p: Report(id=i, **p.model_dump()))
