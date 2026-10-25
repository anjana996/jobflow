"""JobFlow API entry point."""

from fastapi import FastAPI


app = FastAPI(title="JobFlow")


@app.get("/health")
async def health() -> dict[str, str]:
    """Report that the API process is running."""
    return {"status": "ok"}
