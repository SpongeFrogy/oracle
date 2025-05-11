from pydantic import BaseModel


class Token(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Schema for token payload."""

    sub: str | None = None
