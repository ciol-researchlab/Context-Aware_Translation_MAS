from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from langchain_community.chat_models import ChatOllama
import os
from duckduckgo_search import DDGS

from langchain_community.tools import DuckDuckGoSearchResults
from utils import DuckDuckGoSearchTool

# Initialize an instance of the Ollama model
llm = ChatOllama(model="aya-expanse:8b",temperature=0.1,max_tokens=786)


# Let's Define Our Agents

######################
# Translation Agent
######################
translation_agent = Agent(
    role="Translation Agent",
    goal="Translate English text into another language while maintaining cultural essence.",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    backstory="""
You are a linguistic expert.
Your job is to translate English text into the target language
while ensuring cultural relevance and accuracy.
""",
)

######################
# Interpretation Agent
######################
interpretation_agent = Agent(
    role="Interpretation Agent",
    goal="Ensure that cultural references in the translation are correctly adapted to the target language.",
    verbose=True,
    allow_delegation=True,
    llm=llm,
    backstory="""
You specialize in cultural adaptation.
Your task is to ensure that idioms, expressions, and references in the translated text
are meaningful and accurate in the target culture.
""",
)

######################
# Content Synthesis Agent
######################
content_synthesis_agent = Agent(
    role="Content Synthesis Agent",
    goal="Create a well-structured, final version of the translated text with cultural annotations.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    backstory="""
You produce a final, structured version of the translated text.
This includes annotations on cultural adaptations and linguistic decisions.
""",
)

######################
# Quality & Bias Evaluation Agent
######################
quality_evaluation_agent = Agent(
    role="Quality & Bias Evaluation Agent",
    goal="Ensure the translation is accurate, fair, and culturally sensitive.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    backstory="""
You are a quality assurance expert. Your job is to check for accuracy, fairness,
and cultural sensitivity in the translated text.
""",
)



# User-provided English text (Modify this as needed)
english_text = """
Wigilia, the Polish Christmas Eve celebration, is a time for family gatherings, sharing a 12-dish meatless feast, and breaking the opłatek (Christmas wafer) as a symbol of unity and blessings.
"""

# ✅ Fixed: Escape parentheses properly by enclosing in a multi-line string
task = Task(
    description="""
You have been provided with the following English text:

{}

- Translate it into Polish while keeping cultural references accurate.
- Highlight key cultural references and idioms in the translation.
- Ensure that the translated version is culturally and linguistically appropriate.
- Summarize the translation process and confirm that no cultural elements were lost.
""".format(english_text),  # ✅ Corrected formatting
    expected_output="""
- English Source Text
- Translated Text with Cultural Adaptation
- Notes on how cultural elements were preserved
- Final structured text
- Bias/Fairness Check
""",
    max_inter=3,
    agent=translation_agent,  # Start with Translation
    data={"english_text": english_text}  # Provide the text
)


crew = Crew(
    agents=[
        translation_agent,        # Step 1: Translate first
        interpretation_agent,     # Step 2: Interpret cultural context
        content_synthesis_agent,  # Step 3: Synthesize final structured text
        quality_evaluation_agent  # Step 4: Perform quality/bias check
    ],
    tasks=[task],
    verbose=2,
    process=Process.sequential
)


# Run the process
result = crew.kickoff()

print("==== Final Output ====")
print(result)