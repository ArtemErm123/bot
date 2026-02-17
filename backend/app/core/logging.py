import logging


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def get_audit_logger() -> logging.Logger:
    return logging.getLogger("audit")
