from pydantic import BaseModel, Field
from src.schemas.actions import Action


class ActionDTO(BaseModel):
    """Data transfer object."""

    action: Action = Field(description="Action to execute")
    payload: dict = Field(default={}, description="Data")


class ActionResponse(BaseModel):
    data: dict = Field(description="Response data")
