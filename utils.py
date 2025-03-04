# Importing the BaseTool class from the crewai_tools module
from crewai_tools import BaseTool

# Importing the DDGS class from the duckduckgo_search module
from duckduckgo_search import DDGS
from langchain_community.tools import DuckDuckGoSearchResults

# Importing the Type class from the typing module for type annotations
from typing import Type

# Defining a new class DuckDuckGoSearchTool that inherits from BaseTool
class DuckDuckGoSearchTool(BaseTool):
    # Defining the name of the tool
    name: str = "DuckDuckGo Search"

    # Providing a description of what the tool does
    description: str = "Performs web searches using DuckDuckGo."

    # Optional: Defining the maximum number of search results to retrieve
    max_results: int = 5

    # Overriding the _run method to implement the tool's functionality
    def _run(self, query: str) -> str:
        """Search DuckDuckGo and return formatted results."""
        try:
            # Creating an instance of the DDGS class to perform the search
            results = DDGS().text(query, max_results=self.max_results)

            # Formatting the search results into a readable string
            formatted_results = "\n\n".join(
                [f"Title: {res['title']}\nURL: {res['href']}\nSnippet: {res['body']}"
                 for res in results]
            )

            # Returning the formatted results
            return formatted_results
        except Exception as e:
            # Handling any exceptions that occur during the search
            return f"Search failed: {str(e)}"