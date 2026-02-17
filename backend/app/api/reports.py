from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import FileResponse

from app.schemas.report import GenerateReportRequest, GenerateReportResponse, ReportStatusResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_service(request: Request) -> ReportService:
    service = getattr(request.app.state, "report_service", None)
    if not isinstance(service, ReportService):
        raise HTTPException(status_code=500, detail="Report service is not configured")
    return service


@router.post("/generate", response_model=GenerateReportResponse)
def generate_report(
    request: GenerateReportRequest,
    background_tasks: BackgroundTasks,
    service: ReportService = Depends(get_report_service),
) -> GenerateReportResponse:
    report = service.create_report(kind=request.kind, format_=request.format)
    background_tasks.add_task(service.process_report, report.id, request.payload)
    return GenerateReportResponse(report_id=report.id, status=report.status)


@router.get("/{report_id}", response_model=ReportStatusResponse)
def get_report_status(report_id: str, service: ReportService = Depends(get_report_service)) -> ReportStatusResponse:
    try:
        report = service.get_report(report_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    artifact_url = f"/reports/{report.id}/artifact" if report.file_path else None
    return ReportStatusResponse(
        report_id=report.id,
        status=report.status,
        artifact_url=artifact_url,
        file_path=report.file_path,
        metadata=report.generation_metadata,
        error=report.error,
        created_at=report.created_at,
        updated_at=report.updated_at,
    )


@router.get("/{report_id}/artifact")
def get_report_artifact(report_id: str, service: ReportService = Depends(get_report_service)) -> FileResponse:
    try:
        report = service.get_report(report_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if report.file_path is None:
        raise HTTPException(status_code=409, detail="Artifact is not generated yet")

    path = Path(report.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Artifact file is missing")

    return FileResponse(path)
