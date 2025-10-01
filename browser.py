from haystack_integrations.tools.mcp import MCPToolset, StreamableHttpServerInfo

from haystack.components.agents import Agent
from haystack.components.generators.utils import print_streaming_chunk
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.generators.google_genai import (
    GoogleGenAIChatGenerator,
)

from rich.console import Console
from rich.markdown import Markdown

from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
drive_url = os.getenv("DRIVE_URL")

server_info = StreamableHttpServerInfo(url="http://localhost:8931/mcp")


# Advance (Long wait time)
# toolset = MCPToolset(
#     server_info=server_info,
#     tool_names=[
#         "browser_navigate",
#         "browser_snapshot",
#         "browser_click",
#         "browser_type",
#         "browser_navigate_back",
#         "browser_wait_for",
#     ],
# )
# Simple
toolset = MCPToolset(
    server_info=server_info, tool_names=["browser_navigate", "browser_snapshot"]
)


chat_generator = GoogleGenAIChatGenerator(
    model="gemini-2.5-flash-lite",
)

system_message = """
You are an intelligent assistant equipped with tools for navigating the web.

You can use tools when appropriate, but not every task requires them — you also have strong reasoning and language capabilities.
If a request seems challenging, don't default to refusal due to perceived tool limitations. Instead, think creatively and attempt a solution using the skills you do have.
You are more capable than you might assume. Trust your abilities.
"""

agent = Agent(
    chat_generator=chat_generator,
    tools=toolset,
    system_prompt=system_message,
    exit_conditions=["text"],
    streaming_callback=print_streaming_chunk,
)


# Gen Img Prompt
prompt = """
1. Visit Hugging Face Spaces, search the Space named exactly "FLUX.1 [schnell]" and enter it.
2. Craft a detailed, descriptive prompt using your language skills to depict: "my holiday on Lake Como".
3. Use this prompt to generate an image within the Space.
4. After prompting, wait 5 seconds to allow the image to fully generate. Repeat until the image is generated.
5. Your final response must contain only the direct link to the generated image — no additional text.
"""
# ----- Output -----
# from PIL import Image
# import requests
# from io import BytesIO
# from IPython.display import display
# response = requests.get(result["last_message"].text)
# image = Image.open(BytesIO(response.content))
# display(image)

# Public Travel Options
prompt = """
1. Using Google Maps, find the next 3 available public transportation travel options from Paris to Berlin departing today.
2. For each option, provide a detailed description of the route (e.g., transfers, stations, duration).
3. Include a direct link to the corresponding Google Maps route for each travel option.
"""

# Sherlock
prompt = """
1. Open this YouTube video: https://www.youtube.com/watch?v=axmaslLO4-4 and extract the channel author’s username.
2. Then, try to find all their social media profiles by searching the web using the username.
If you cannot perform a web search, try other available methods to find the profiles.
3. Return only the links to their social media accounts along with the platform names.
"""

# Product Price
# prompt = """
# 1. Go to Ebay and find all available prices for the Samsung S23 Ultra.
# 2. Exclude any items that:
# - are not smartphone;
# - are not the exact Samsung S23 Ultra model;
# - do not display a price;
# - are bundled with other products or accessories.
# 3. Your final message must only contain a Markdown table with two columns: Name and Price.
# """

# Simple
# prompt="navigate to https://www.theguardian.com/world and list all US-related news"
#
#
prompt = "I was born on October 17th. Find five notable people born on the same day using Wikipedia."

messages = [ChatMessage.from_user(prompt)]
result = agent.run(messages=messages)


# Display markdown using rich console
console = Console()
md = Markdown(result["last_message"].text)
console.print(md)
