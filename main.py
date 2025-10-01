import os

from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import ComponentTool
from haystack.components.websearch import SerperDevWebSearch

from haystack_integrations.components.generators.google_genai import (
    GoogleGenAIChatGenerator,
)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

search_tool = ComponentTool(component=SerperDevWebSearch())

basic_agent = Agent(
    chat_generator=GoogleGenAIChatGenerator(model="gemini-2.5-flash"),
    system_prompt="You are a helpful web agent.",
    tools=[search_tool],
)

result = basic_agent.run(
    messages=[ChatMessage.from_user("When was the first version of Haystack released?")]
)

print(result["last_message"].text)
