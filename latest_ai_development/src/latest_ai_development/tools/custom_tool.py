
from crewai.tools import BaseTool
from typing import Type,Union,Any,Dict,List
from pydantic import BaseModel, Field
from langchain_community.tools.gmail.send_message import GmailSendMessage
from fastapi import FastAPI
app = FastAPI()
from langchain_community.tools.gmail.utils import get_gmail_credentials,build_resource_service

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: Union[str, Dict[str, Any]] = Field(..., description="Tell us what the users wants to answer")

class HumanTool(BaseTool):
    name: str = "Human interact"
    description: str = "Ask questions to the user to collect information"
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: Union[str, Dict[str, Any]]) -> str:
        if isinstance(argument, dict):
            description = argument.get("description")
            if not description:  # If "description" key is missing or empty
                return "Invalid input: Missing description key. Please provide a valid prompt."
            return input(f"{description} \n")
    
        if isinstance(argument, str) and argument.strip():
            return input(f"{argument.strip()} \n")
    
    # Fallback if argument is neither string nor dict or is invalid
        return "Invalid input provided. Please check the input format."
    
class CreateDraftTool(BaseTool):
    name: str = "Email Sending Tool"
    description: str = (
        """
          Useful to create an email draft and send it too.
            The input to this tool should be a pipe (|) separated text
            of length 3 (three), representing who to send the email to,
            the subject of the email and the actual message.
            For example, `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`.
            and also send the email
        """
        )
    def _run(self,argument:str) -> str:
        try:
            parts = argument.split("|")
            if len(parts) != 3:
                raise ValueError("Input must contain exactly two '|' separators.")
            email, subject, message = parts
        except ValueError as e:
            return f"Error: Invalid input format. {str(e)}"
        email, subject, message = argument.split("|")
        credentials = get_gmail_credentials(client_secrets_file="/mnt/c/Users/sanni/OneDrive/Desktop/Priti/mailingsys/latest_ai_development/Credentials.json")
        api_resource = build_resource_service(credentials=credentials)
        draft2 = GmailSendMessage(api_resource=api_resource)
        result2 = draft2({"to": [email], "subject": subject, "message": message})
        return f"Email Sent {result2}"

