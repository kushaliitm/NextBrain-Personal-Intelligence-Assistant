# NextBrain - Personal Intelligence Assistant

> A sophisticated multi-agent AI system that orchestrates intelligent personal assistants to manage your email, calendar, tasks, research, and more through a unified interface.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[Overview](#overview) • [Features](#features) • [Architecture](#architecture) • [Installation](#installation) • [Configuration](#configuration) • [Usage](#usage) • [API Reference](#api-reference) • [Contributing](#contributing)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
  - [System Design](#system-design)
  - [Agent Hierarchy](#agent-hierarchy)
  - [Data Flow](#data-flow)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Google OAuth Setup](#google-oauth-setup)
  - [API Configuration](#api-configuration)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Agent Configuration](#agent-configuration)
- [Usage](#usage)
  - [Quick Start](#quick-start)
  - [Running the Assistant](#running-the-assistant)
  - [Integration Channels](#integration-channels)
- [Agents Overview](#agents-overview)
  - [Manager Agent](#manager-agent)
  - [Email Agent](#email-agent)
  - [Calendar Agent](#calendar-agent)
  - [Notion Agent](#notion-agent)
  - [Researcher Agent](#researcher-agent)
  - [Slack Agent](#slack-agent)
- [Tools & Capabilities](#tools--capabilities)
  - [Email Tools](#email-tools)
  - [Calendar Tools](#calendar-tools)
  - [Notion Tools](#notion-tools)
  - [Research Tools](#research-tools)
  - [Communication Tools](#communication-tools)
- [API Reference](#api-reference)
  - [Core Classes](#core-classes)
  - [Agent Methods](#agent-methods)
  - [Tool Functions](#tool-functions)
- [Examples](#examples)
  - [Task Examples](#task-examples)
  - [Advanced Scenarios](#advanced-scenarios)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

NextBrain is an advanced personal intelligence assistant powered by LangChain and LangGraph. It uses a hierarchical multi-agent architecture where specialized agents collaborate to handle complex tasks across multiple platforms and services.

**The system enables you to:**
- Manage your email inbox intelligently (Gmail)
- Organize and manage your calendar (Google Calendar)
- Handle your to-do lists and tasks (Notion)
- Research information across the web
- Search and scrape LinkedIn profiles
- Integrate with multiple communication channels (WhatsApp, Telegram, Slack)

The architecture uses a **Manager Agent** that orchestrates specialized sub-agents, delegating tasks appropriately and ensuring quality assurance. All inter-agent communication is facilitated through a unified messaging framework.

---

## Key Features

### 🤖 Multi-Agent Architecture
- **Manager Agent**: Central orchestrator that delegates tasks to specialized sub-agents
- **Specialized Agents**: Email, Calendar, Notion, Research, and Slack agents with specific expertise
- **LangChain Integration**: Built on LangChain's ReAct (Reasoning + Acting) framework
- **Agent Memory**: SQLite-based persistent memory for the manager agent

### 📧 Email Management
- Read emails with date filtering
- Send emails with attachments support
- Find contact information from your email
- Extract and parse email content

### 📅 Calendar Management
- View calendar events within date ranges
- Create new events with detailed descriptions
- Check availability before scheduling
- Automatic timezone handling

### ✅ Task Management
- Sync with Notion for to-do list management
- Add tasks with due dates
- Retrieve and organize tasks
- Integration with personal workflow

### 🔍 Research & Intelligence
- Web search with multiple search engines
- Website scraping and content extraction
- LinkedIn profile research
- Company information lookup

### 💬 Multi-Channel Communication
- WhatsApp integration via Twilio
- Telegram bot support
- Slack channel integration
- Unified message handling

### 🔧 Extensibility
- Easy to add new agents
- Plugin-based tool architecture
- Support for multiple LLM providers (OpenAI, Groq, etc.)
- Custom prompt engineering

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│           Communication Channels (WhatsApp, Telegram, Slack) │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     Manager Agent                            │
│    (Orchestrator with SQLite Memory & Checkpointing)        │
│                                                              │
│  • Task Analysis & Delegation                               │
│  • Quality Assurance                                         │
│  • Response Compilation                                      │
└─────────────────────────────────────────────────────────────┘
       │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼
  ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
  │ Email  ││Calendar││ Notion ││Research││ Slack  │
  │ Agent  ││ Agent  ││ Agent  ││ Agent  ││ Agent  │
  └────────┘└────────┘└────────┘└────────┘└────────┘
       │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼
    Gmail   Google Cal  Notion API  Web APIs  Slack API
```

### Agent Hierarchy

- **Tier 1 - Manager Agent**: 
  - Central decision-making unit
  - Uses GPT-4 (OpenAI) for complex reasoning
  - Maintains conversation history via SQLite
  - Delegates to sub-agents using SendMessage tool

- **Tier 2 - Specialized Agents** (GPT-4o Mini):
  - Email Agent: Gmail integration
  - Calendar Agent: Google Calendar integration
  - Notion Agent: Notion API integration
  - Researcher Agent: Web search and scraping
  - Slack Agent: Slack integration

### Data Flow

```
User Input (via Channel)
        │
        ▼
Manager Agent receives message
        │
        ├─► Analyzes task requirements
        ├─► Determines which agent(s) needed
        │
        ▼
SendMessage to Sub-Agent(s)
        │
        ▼
Sub-Agent processes request
        ├─► Uses specialized tools
        ├─► Interacts with external APIs
        │
        ▼
Response returned to Manager
        │
        ├─► Quality check
        ├─► Format response
        │
        ▼
Send result back to user
```

---

## Project Structure

```
NextBrain-Personal-Intelligence-Assistant/
├── src/
│   ├── agents/
│   │   ├── base/
│   │   │   ├── __init__.py           # Base agent and orchestrator exports
│   │   │   ├── agent.py              # Core Agent class
│   │   │   └── agents_orchestrator.py # Orchestration logic
│   │   └── personal_assistant.py      # PersonalAssistant main class
│   │
│   ├── channels/
│   │   └── whatsapp.py               # WhatsApp integration via Twilio
│   │
│   ├── prompts/
│   │   ├── __init__.py               # Prompt exports
│   │   ├── manager_agent.py           # Manager prompt & SOP
│   │   ├── email_agent.py             # Email agent system prompt
│   │   ├── calendar_agent.py          # Calendar agent system prompt
│   │   ├── notion_agent.py            # Notion agent system prompt
│   │   ├── researcher_agent.py        # Research agent system prompt
│   │   └── slack_agent.py             # Slack agent system prompt
│   │
│   ├── tools/
│   │   ├── send_message.py           # Inter-agent communication tool
│   │   │
│   │   ├── email/
│   │   │   ├── __init__.py
│   │   │   ├── read_emails.py        # Read and filter emails
│   │   │   ├── send_email.py         # Send email functionality
│   │   │   └── find_contacts.py      # Find contact email addresses
│   │   │
│   │   ├── calendar/
│   │   │   ├── __init__.py
│   │   │   ├── get_events.py         # Retrieve calendar events
│   │   │   └── create_event.py       # Create calendar events
│   │   │
│   │   ├── notion/
│   │   │   ├── __init__.py
│   │   │   ├── get_tasks.py          # Retrieve Notion tasks
│   │   │   └── add_task.py           # Add tasks to Notion
│   │   │
│   │   └── research/
│   │       ├── __init__.py
│   │       ├── search_web.py         # Web search functionality
│   │       ├── scrape_website.py     # Website content scraping
│   │       └── search_linkedin.py    # LinkedIn profile research
│   │
│   └── utils.py                       # Utility functions & Google OAuth
│
├── credentials.json                   # Google OAuth credentials
├── token.json                         # Google OAuth token (auto-generated)
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

---

## Installation & Setup

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Package manager
- **Git**: For cloning the repository
- **Google Account**: For Gmail and Google Calendar
- **Notion Account**: For task management (optional)
- **API Keys**: OpenAI, Google Cloud, Tavily, Serper (see Configuration)

### Environment Setup

1. **Clone the repository:**
```bash
git clone https://github.com/kushaliitm/NextBrain-Personal-Intelligence-Assistant.git
cd NextBrain-Personal-Intelligence-Assistant
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Google OAuth Setup

This project requires Google OAuth for Gmail and Google Calendar access.

1. **Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Gmail API and Google Calendar API

2. **Create OAuth 2.0 Credentials:**
   - In the Google Cloud Console, go to "Credentials"
   - Create a new "OAuth 2.0 Client ID" (Desktop application)
   - Download the credentials file as `credentials.json`
   - Place it in the project root directory

3. **First-time authentication:**
   - Run the application once
   - A browser window will open asking for Gmail and Calendar permissions
   - Authorize the application
   - A `token.json` file will be automatically created

### API Configuration

Obtain the following API keys and add them to your `.env` file (see Configuration section).

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (use `.env.example` as template):

```dotenv
# ==================== LLM & AI Services ====================
OPENAI_API_KEY=sk-proj-...                 # OpenAI API key for GPT models
GROQ_API_KEY=gsk_...                       # Groq API key (alternative LLM)
GOOGLE_API_KEY=AIzaSy...                   # Google Cloud API key

# ==================== LangChain Configuration ====================
LANGCHAIN_TRACING_V2=true                  # Enable LangSmith tracing
LANGCHAIN_API_KEY=lsv2_pt_...             # LangSmith API key
LANGCHAIN_PROJECT=Personal                 # Project name in LangSmith

# ==================== Search & Research ====================
TAVILY_API_KEY=tvly--dev-...              # Tavily API for web search
SERPER_API_KEY=A017fdb...                 # Serper API for search results

# ==================== Gmail Configuration ====================
GMAIL_MAIL=your-email@gmail.com            # Gmail address
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx     # 16-character app password

# ==================== Notion Configuration ====================
NOTION_TOKEN=ntn_...                       # Notion API token
NOTION_DATABASE_ID=2e3c687f...            # Notion database ID for tasks

# ==================== Communication Channels ====================
TWILIO_ACCOUNT_SID=AC...                   # Twilio account SID
TWILIO_AUTH_TOKEN=...                      # Twilio auth token
FROM_WHATSAPP_NUMBER=whatsapp:+...        # WhatsApp sender number

# Optional - Telegram & Slack configuration can be added here
# TELEGRAM_TOKEN=...
# CHAT_ID=...
```

### Agent Configuration

Agents are configured in [src/agents/personal_assistant.py](src/agents/personal_assistant.py):

```python
email_agent = Agent(
    name="email_agent",
    description="Email agent can manage GMAIL inbox",
    model="openai/gpt-4o-mini",
    system_prompt=EMAIL_AGENT_PROMPT.format(date_time=get_current_date_time()),
    tools=[read_emails, send_email, find_contact_email],
    temperature=0.1  # Lower = more deterministic
)
```

**Key Configuration Options:**
- `name`: Agent identifier
- `model`: LLM to use (format: "provider/model")
- `temperature`: Creativity level (0.0-1.0)
- `tools`: Available tools for the agent
- `system_prompt`: Agent instructions and SOP

---

## Usage

### Quick Start

1. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. **Run initial setup:**
```bash
python -c "from src.utils import get_credentials; get_credentials()"
# This will prompt you to authorize Google access
```

3. **Initialize and test:**
```python
from src.agents import PersonalAssistant
import sqlite3

# Create database connection
db = sqlite3.connect(":memory:")

# Initialize the assistant
assistant = PersonalAssistant(db)

# Send a request
response = assistant.invoke("Check my emails from today")
print(response)
```

### Running the Assistant

```python
from src.agents import PersonalAssistant
import sqlite3

# Initialize
db_connection = sqlite3.connect("nextbrain.db")
assistant = PersonalAssistant(db_connection)

# Make a request - the manager will orchestrate sub-agents
response = assistant.invoke("Schedule a meeting with John next Tuesday at 2 PM")

# Stream responses for real-time feedback
for chunk in assistant.stream("Find research articles about AI safety"):
    print(chunk, end="", flush=True)
```

### Integration Channels

#### WhatsApp Integration (Twilio)
```python
from src.channels import WhatsAppChannel

whatsapp = WhatsAppChannel()
whatsapp.send_message(
    to_number="+1234567890",
    body="Hello from NextBrain!"
)
```

#### Telegram Integration
The system can be connected to Telegram bots using webhooks and the Telegram Bot API.

#### Slack Integration
Connect to Slack workspaces for task delegation and updates.

---

## Agents Overview

### Manager Agent

**Role:** Central orchestrator and decision maker

**Capabilities:**
- Analyze incoming tasks
- Delegate to appropriate sub-agents
- Verify sub-agent outputs
- Compile and format responses
- Maintain conversation history (SQLite)

**Model:** OpenAI GPT-4 (for complex reasoning)
**Memory:** SQLite checkpointer for persistent state

**Responsibilities (SOP):**
1. Evaluate task requirements
2. Break down complex tasks
3. Delegate to sub-agents using SendMessage
4. Verify outputs for accuracy
5. Report results back to user

### Email Agent

**Role:** Gmail inbox management

**Capabilities:**
- Read emails with date filtering
- Send emails with subjects and body
- Find contact email addresses

**Model:** OpenAI GPT-4o Mini
**Tools:**
- `read_emails(from_date, to_date, email)` - Retrieve emails
- `send_email(to, subject, body)` - Send emails
- `find_contact_email(name)` - Find email addresses

**Example Tasks:**
- "Send an email to John about the project deadline"
- "Read my emails from Monday"
- "Find the email address for Sarah Johnson"

### Calendar Agent

**Role:** Google Calendar management

**Capabilities:**
- View events within date ranges
- Create new calendar events
- Check availability
- Handle event details and descriptions

**Model:** OpenAI GPT-4o Mini
**Tools:**
- `get_calendar_events(start_date, end_date)` - List events
- `add_event_to_calendar(title, description, start_time)` - Create events
- `find_contact_email(name)` - For participant lookup

**Example Tasks:**
- "Show my calendar for next week"
- "Create a meeting with the team on Friday at 3 PM"
- "Am I free on Tuesday afternoon?"

### Notion Agent

**Role:** Task and project management

**Capabilities:**
- Add tasks to to-do list
- Retrieve existing tasks
- Organize by date

**Model:** OpenAI GPT-4o Mini
**Tools:**
- `get_my_todo_list(date)` - Retrieve tasks
- `add_task_in_todo_list(task, date)` - Add tasks

**Example Tasks:**
- "Add 'Review presentation' to my to-do list"
- "Show my tasks for today"
- "Create a task for project planning on Friday"

### Researcher Agent

**Role:** Information research and intelligence gathering

**Capabilities:**
- Web search with multiple sources
- Website content scraping
- LinkedIn profile research
- Company information lookup

**Model:** OpenAI GPT-4o Mini
**Tools:**
- `search_web(query, search_type, max_results)` - Web search
- `scrape_website_to_markdown(url)` - Content extraction
- `search_linkedin_tool(person_name, company_name)` - LinkedIn research

**Example Tasks:**
- "Research company information about Tesla"
- "Find LinkedIn profile of Sarah Johnson at Microsoft"
- "Scrape and summarize content from example.com"
- "Search for 'machine learning trends 2025'"

### Slack Agent

**Role:** Slack workspace integration

**Capabilities:**
- Read Slack messages
- Send messages to channels/DMs
- Channel integration
- Team collaboration

**Example Tasks:**
- "Send a message to #general about the meeting"
- "Read messages from #engineering"

---

## Tools & Capabilities

### Email Tools

#### read_emails
Retrieves emails from Gmail inbox with optional filtering.

```python
from src.tools.email import read_emails

# Get emails from specific date range
emails = read_emails(
    from_date="2025-01-01",
    to_date="2025-01-10",
    email="specific@email.com"  # Optional filter
)
```

**Parameters:**
- `from_date` (str): Start date (YYYY-MM-DD format)
- `to_date` (str): End date (YYYY-MM-DD format)
- `email` (Optional[str]): Filter by sender email

**Returns:** List of email dictionaries with subject, sender, date, and content

#### send_email
Sends an email via Gmail.

```python
from src.tools.email import send_email

response = send_email(
    to="recipient@email.com",
    subject="Meeting Confirmation",
    body="Hi, confirming our meeting at 2 PM..."
)
```

**Parameters:**
- `to` (str): Recipient email address
- `subject` (str): Email subject
- `body` (str): Email body content

**Returns:** Confirmation message

#### find_contact_email
Finds email addresses for contacts.

```python
from src.tools.email import find_contact_email

email = find_contact_email("John Doe")
```

**Parameters:**
- `name` (str): Contact name

**Returns:** Email address string

### Calendar Tools

#### get_calendar_events
Retrieves events from Google Calendar.

```python
from src.tools.calendar import get_calendar_events

events = get_calendar_events(
    start_date="2025-01-15",
    end_date="2025-01-22"
)
```

**Parameters:**
- `start_date` (str): Start date (YYYY-MM-DD format)
- `end_date` (str): End date (YYYY-MM-DD format)

**Returns:** List of calendar events with title, time, description

#### add_event_to_calendar
Creates a new calendar event.

```python
from src.tools.calendar import add_event_to_calendar

result = add_event_to_calendar(
    title="Team Standup",
    description="Daily standup meeting",
    start_time="2025-01-15 10:00 AM"
)
```

**Parameters:**
- `title` (str): Event title
- `description` (str): Event description
- `start_time` (str): Start time (YYYY-MM-DD HH:MM AM/PM format)

**Returns:** Confirmation message

### Notion Tools

#### get_my_todo_list
Retrieves tasks from Notion for a specific date.

```python
from src.tools.notion import get_my_todo_list

tasks = get_my_todo_list(date="2025-01-15")
```

**Parameters:**
- `date` (str): Date to retrieve tasks (YYYY-MM-DD format)

**Returns:** List of tasks with due dates and status

#### add_task_in_todo_list
Adds a new task to Notion.

```python
from src.tools.notion import add_task_in_todo_list

result = add_task_in_todo_list(
    task="Complete project proposal",
    date="2025-01-20"
)
```

**Parameters:**
- `task` (str): Task description
- `date` (str): Due date (YYYY-MM-DD format)

**Returns:** Confirmation message

### Research Tools

#### search_web
Performs web search using multiple search engines.

```python
from src.tools.research import search_web

results = search_web(
    query="AI safety 2025",
    search_type="basic",
    max_results=5
)
```

**Parameters:**
- `query` (str): Search query
- `search_type` (str): "basic" or "advanced" (default: "basic")
- `max_results` (int): Number of results (default: 5)

**Returns:** List of search results with URLs and snippets

#### scrape_website_to_markdown
Scrapes and converts website content to markdown.

```python
from src.tools.research import scrape_website_to_markdown

content = scrape_website_to_markdown(url="https://example.com/article")
```

**Parameters:**
- `url` (str): Website URL to scrape

**Returns:** Markdown formatted content

#### search_linkedin_tool
Searches for LinkedIn profiles using Google and scrapes data.

```python
from src.tools.research import search_linkedin_tool

profile = search_linkedin_tool(
    person_name="John Doe",
    company_name="Microsoft"
)
```

**Parameters:**
- `person_name` (Optional[str]): Person's name
- `company_name` (str): Company name

**Returns:** LinkedIn profile information

### Communication Tools

#### SendMessage
Inter-agent communication tool for manager to delegate tasks.

```python
# Used internally by Manager Agent
response = send_message(
    recipient="email_agent",
    message="Send an email to john@example.com about the deadline"
)
```

**Parameters:**
- `recipient` (str): Target agent name
- `message` (str): Task message

**Returns:** Agent response

---

## API Reference

### Core Classes

#### PersonalAssistant

Main class to initialize the complete system.

```python
from src.agents import PersonalAssistant

assistant = PersonalAssistant(db_connection)
```

**Methods:**
- `invoke(message, **kwargs)` - Send synchronous request
- `stream(message, **kwargs)` - Stream responses for real-time feedback

#### Agent

Base agent class for creating specialized agents.

```python
from src.agents.base import Agent

agent = Agent(
    name="custom_agent",
    description="Description of the agent",
    system_prompt="System instructions",
    tools=[tool1, tool2],
    sub_agents=[],
    model="openai/gpt-4o-mini",
    temperature=0.1,
    memory=None
)
```

**Parameters:**
- `name` (str): Agent identifier
- `description` (str): Agent description
- `system_prompt` (str): System instructions
- `tools` (List): Available tools
- `sub_agents` (List[Agent]): Sub-agents (empty for leaf agents)
- `model` (str): LLM model in "provider/model" format
- `temperature` (float): LLM temperature (0.0-1.0)
- `memory`: Optional memory storage

**Methods:**
- `invoke(*args, **kwargs)` - Synchronous invocation
- `stream(*args, **kwargs)` - Streaming invocation

#### AgentsOrchestrator

Manages agent communication and coordination.

```python
from src.agents.base import AgentsOrchestrator

orchestrator = AgentsOrchestrator(
    main_agent=manager_agent,
    agents=[agent1, agent2, agent3]
)
```

**Methods:**
- `invoke(message, **kwargs)` - Send message to orchestrator
- `stream(message, **kwargs)` - Stream responses

### Agent Methods

#### invoke(message, **kwargs)
Synchronously send a message to an agent and get response.

```python
response = agent.invoke({"messages": [("human", "Your message")]})
print(response["messages"][-1].content)
```

#### stream(message, **kwargs)
Stream responses from an agent for real-time feedback.

```python
for chunk in agent.stream({"messages": [("human", "Your message")]}):
    print(chunk, end="", flush=True)
```

---

## Examples

### Task Examples

#### 1. Schedule a Meeting
```python
from src.agents import PersonalAssistant
import sqlite3

db = sqlite3.connect(":memory:")
assistant = PersonalAssistant(db)

# Manager will delegate to Calendar and Email agents
response = assistant.invoke(
    "Schedule a meeting with Sarah Johnson on Friday at 3 PM to discuss the Q1 roadmap"
)
print(response)
```

#### 2. Research and Report
```python
response = assistant.invoke(
    "Research the latest trends in AI and send me a summary"
)
```

The Researcher Agent will:
1. Search the web for AI trends
2. Scrape relevant articles
3. Compile a summary
4. Manager returns the report

#### 3. Manage Tasks
```python
response = assistant.invoke(
    "Add 'Review quarterly goals' to my to-do list for next Monday, "
    "and remind me about the client meeting at 2 PM"
)
```

#### 4. Email Management
```python
response = assistant.invoke(
    "Check my emails from the past week and summarize any urgent items"
)
```

#### 5. LinkedIn Research
```python
response = assistant.invoke(
    "Find LinkedIn profiles for John Smith at Google and Sarah Davis at Meta"
)
```

### Advanced Scenarios

#### Complex Multi-Task Orchestration
```python
response = assistant.invoke(
    """
    I need your help with the following:
    1. Check my calendar for next week
    2. Find any overlapping commitments
    3. Research the attendees from my LinkedIn
    4. Send them a brief intro message
    5. Add follow-up tasks to my Notion
    """
)
```

#### Conditional Task Routing
```python
response = assistant.invoke(
    "If I have any emails from my CEO, forward them to my team. "
    "Also, schedule a debrief meeting for tomorrow at 4 PM."
)
```

#### Data Integration
```python
response = assistant.invoke(
    "Create a report of next week's meetings with LinkedIn profiles "
    "of all attendees and save it as a task in my Notion workspace"
)
```

---

## Troubleshooting

### Common Issues

#### 1. Google OAuth Authentication Fails
**Problem:** "Invalid credentials" or token refresh fails

**Solution:**
```bash
# Delete existing tokens and re-authenticate
rm token.json
python -c "from src.utils import get_credentials; get_credentials()"
```

#### 2. API Rate Limits
**Problem:** "Rate limit exceeded" errors

**Solution:**
- Increase delays between API calls
- Use more specific search queries
- Consider upgrading API plans

#### 3. Agent Not Responding
**Problem:** Agent returns empty response

**Solution:**
```python
# Check if agent is initialized
if not agent.agent:
    agent.initiat_agent()

# Verify tools are available
print(agent.tools)

# Check API keys in environment
import os
print(os.getenv("OPENAI_API_KEY"))
```

#### 4. Memory Issues with Manager Agent
**Problem:** SQLite checkpointer errors

**Solution:**
```python
# Use in-memory database for testing
import sqlite3
db = sqlite3.connect(":memory:")

# For production, use file-based database
db = sqlite3.connect("nextbrain.db")
```

#### 5. Email Not Sending
**Problem:** "Failed to send email"

**Solution:**
- Verify Gmail app password (not regular password)
- Enable "Less secure app access" if needed
- Check email format validation

### Debugging

Enable LangSmith tracing for detailed debugging:

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"

# Now run agents for detailed trace
response = assistant.invoke("Your message")
# Check LangSmith dashboard for trace details
```

---

## Contributing

We welcome contributions! Here's how to get started:

### Development Setup
```bash
# Clone and setup
git clone <repo>
cd NextBrain-Personal-Intelligence-Assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Adding a New Agent

1. **Create agent file** in `src/agents/`
2. **Define system prompt** in `src/prompts/`
3. **Register agent** in `PersonalAssistant` class
4. **Add to manager's sub_agents** list
5. **Test thoroughly**

### Adding a New Tool

1. **Create tool file** in appropriate `src/tools/` subdirectory
2. **Implement tool function** with proper type hints
3. **Add to agent's tools list**
4. **Document in README**
5. **Test with agent**

### Code Style
- Follow PEP 8
- Add docstrings to all functions
- Use type hints
- Keep functions small and focused

### Commit Guidelines
- Clear, descriptive commit messages
- Reference issues when applicable
- Keep commits atomic and focused

### Pull Request Process
1. Create feature branch from main
2. Make changes with clear commits
3. Update README if adding features
4. Test thoroughly
5. Submit PR with description

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Agent orchestration using [LangGraph](https://langchain-ai.github.io/langgraph/)
- LLM integration with [OpenAI](https://openai.com/)
- Google Workspace integration via official APIs

---

## Support & Contact

For issues, questions, or suggestions:
- 📧 Open an issue on GitHub
- 💬 Check existing discussions
- 📚 Refer to documentation above

---

**Last Updated:** January 2025 | **Version:** 1.0.0

