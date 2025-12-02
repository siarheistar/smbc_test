"""
Data models for the Anagram Checker API
"""
from pydantic import BaseModel, Field


class AnagramRequest(BaseModel):
    """Request model for anagram checking"""
    input1: str = Field(..., description="First string to compare", min_length=1)
    input2: str = Field(..., description="Second string to compare", min_length=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input1": "listen",
                    "input2": "silent"
                }
            ]
        }
    }


class AnagramResponse(BaseModel):
    """Response model for anagram checking"""
    input1: str
    input2: str
    result: bool = Field(..., description="True if strings are anagrams, False otherwise")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input1": "listen",
                    "input2": "silent",
                    "result": True
                }
            ]
        }
    }
