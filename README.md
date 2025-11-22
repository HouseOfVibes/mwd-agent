# MWD Agent

> AI-Powered Workspace Management Agent for MW Design Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![MCP](https://img.shields.io/badge/MCP-1.21.1-purple.svg)](https://modelcontextprotocol.io/)

An intelligent multi-AI agent system that automates business workflows across branding, website design, social media strategy, copywriting, and workspace management. Integrates with Notion, Google Workspace, Slack, and the MWD Invoice System.

## What's New (November 2025)

- **Slack Bot Features**: Conversational AI interface with Gemini orchestration
  - Automated deadline reminders (daily at 9 AM)
  - Activity digests (daily at 6 PM, weekly on Fridays)
  - Quick action buttons for common tasks
  - File upload handling with intelligent suggestions
- **Client Portal Builder**: Create comprehensive Notion portals with service-specific pages
- **35+ API Endpoints**: Full implementation of all AI, integration, and webhook endpoints
- **MCP Integration**: Model Context Protocol for standardized multi-AI coordination
- **Latest Dependencies**: All packages updated to November 2025 versions
  - Claude Sonnet 4.5 (anthropic 0.73.0)
  - Gemini 2.0 Flash (google-genai 1.50.0)
  - GPT-4o/4.1 (openai 2.8.0)
  - MCP SDK 1.21.0
- **7 MCP Servers**: Memory, Git, Supabase, Filesystem, GitHub, PostgreSQL, Sequential Thinking

## Features

- **AI-Powered Strategy Generation**: Branding, website design, social media, and copywriting deliverables
- **Conversational Slack Bot**: Natural language interface with Gemini orchestration
  - Thread-aware context and conversation persistence
  - Automated deadline reminders and activity digests
  - Quick action buttons and file upload handling
- **Client Portal Builder**: Create comprehensive Notion portals with Timeline, Deliverables, Communication Log, and service-specific pages
- **Workspace Intelligence**: Gemini-powered meeting notes, document summarization, and Google Drive organization
- **Multi-AI Orchestration**: Specialized AI routing (Gemini, Claude, GPT-4o, Perplexity)
- **MCP Integration**: Model Context Protocol for standardized AI tool access and multi-agent coordination
- **Persistent Memory**: Long-term memory storage across AI sessions for consistent client context
- **Invoice System Integration**: Automated lead creation, proposal generation, and client portal sync
- **Project Management**: Automated Notion workspace updates and timeline tracking

For a complete list of capabilities, see [MWD_AGENT_CAPABILITIES.md](MWD_AGENT_CAPABILITIES.md).

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           GEMINI (PRIMARY AI - CORE SYSTEM)             │
│  • Notion Workspace Understanding & Sync                │
│  • Google Meet → Automatic Meeting Notes                │
│  • Google Drive → File Organization & Management        │
│  • Action Item Extraction & Tracking                    │
└─────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼─────────┐    ┌───────▼─────────┐
        │     CLAUDE      │    │   CHATGPT +     │
        │   Strategic     │    │   PERPLEXITY    │
        │  Deliverables   │    │  Communication  │
        └─────────────────┘    └─────────────────┘
                │                       │
                └───────────┬───────────┘
                            │
              ┌─────────────▼──────────────┐
              │   MCP (Model Context       │
              │   Protocol) Servers        │
              │  ┌──────────────────────┐  │
              │  │ • Memory (shared)    │  │
              │  │ • Supabase (data)    │  │
              │  │ • Git (repository)   │  │
              │  │ • Filesystem (files) │  │
              │  └──────────────────────┘  │
              └────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+ (tested on 3.11.14)
- Node.js 18+ (for TypeScript MCP servers)
- Anthropic API key (Claude)
- Google Cloud project (for Gemini API)
- Optional: OpenAI API key, Perplexity API key
- Optional: Supabase account, Slack workspace, Notion workspace

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HouseOfVibes/mwd-agent.git
   cd mwd-agent
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the agent**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8080`

## Environment Variables

Create a `.env` file with the following:

```bash
# AI APIs - Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Slack Bot - Required for Slack features
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your_signing_secret
SLACK_APP_TOKEN=xapp-your-app-token

# Slack Channels - Optional (defaults available)
SLACK_REMINDER_CHANNEL=your_reminder_channel_id
SLACK_DIGEST_CHANNEL=your_digest_channel_id

# Notion - Required for Notion features
NOTION_API_KEY=your_notion_api_key_here
NOTION_PORTALS_PAGE=your_portals_parent_page_id
NOTION_PROJECTS_DATABASE=your_projects_database_id

# Google Workspace - Required for Google features
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_CLOUD_PROJECT=your_project_id

# Supabase - Optional
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# Invoice System - Optional
INVOICE_SYSTEM_URL=your_invoice_system_url
INVOICE_SYSTEM_API_KEY=your_api_key

# MCP Servers - Optional
GITHUB_TOKEN=your_github_personal_access_token_here
```

### AI SDK Versions (Latest November 2025)

| Package | Version | Model | Status |
|---------|---------|-------|--------|
| **anthropic** | >=0.73.0 | Claude Sonnet 4.5 | ✅ Active |
| **google-genai** | >=1.50.0 | Gemini 2.0 Flash | ✅ Active |
| **openai** | >=2.8.0 | GPT-4o / GPT-4.1 | ✅ Active |
| **perplexityai** | >=0.20.0 | Sonar Pro | ✅ Active |
| **mcp** | >=1.21.0 | MCP Protocol | ✅ Active |

⚠️ **Important**: `google-generativeai` is **DEPRECATED** (support ends Nov 30, 2025). Use `google-genai` instead.

See [docs/API_INTEGRATION_GUIDE.md](docs/API_INTEGRATION_GUIDE.md) for detailed integration instructions and [.claude/MCP_SETUP.md](.claude/MCP_SETUP.md) for MCP configuration.

## API Endpoints (35+)

### Strategy Generation (Claude)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and service status |
| POST | `/branding` | Generate comprehensive branding strategy |
| POST | `/website` | Create website design plan and sitemap |
| POST | `/social` | Generate social media strategy |
| POST | `/copywriting` | Create marketing copy and messaging |

### AI Services

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/gemini/meeting-notes` | Process meeting transcripts |
| POST | `/ai/gemini/summarize` | Summarize documents |
| POST | `/ai/gemini/orchestrate` | Multi-AI task orchestration |
| POST | `/ai/openai/team-message` | Draft team communications |
| POST | `/ai/openai/slack-message` | Draft Slack messages |
| POST | `/ai/openai/summarize-thread` | Summarize conversation threads |
| POST | `/ai/openai/analyze-feedback` | Analyze feedback sentiment |
| POST | `/ai/perplexity/research` | Research topics with citations |
| POST | `/ai/perplexity/industry` | Industry research |
| POST | `/ai/perplexity/competitors` | Competitor analysis |
| POST | `/ai/perplexity/client-email` | Draft client emails |
| POST | `/ai/perplexity/market-data` | Market data research |

### Notion Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notion/project` | Create project page |
| POST | `/notion/meeting-notes` | Create meeting notes |
| GET | `/notion/search` | Search workspace |
| POST | `/notion/database/query` | Query databases |
| POST | `/notion/page/status` | Update project status |
| POST | `/notion/client-portal` | Build client portal |

### Google Workspace

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/google/drive/folder` | Create folder |
| POST | `/google/drive/project-structure` | Create project folder structure |
| GET | `/google/drive/files` | List files |
| POST | `/google/drive/share` | Share files |
| POST | `/google/docs/document` | Create document |
| POST | `/google/docs/deliverable` | Create formatted deliverable |

### Slack Bot

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/slack/events` | Handle Slack events |
| POST | `/slack/interact` | Handle interactive components |
| POST | `/slack/reminders` | Send deadline reminders |
| POST | `/slack/digest` | Send activity digest |
| POST | `/slack/quick-actions` | Send quick actions menu |

### Webhooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/intake` | Receive client intake forms |
| POST | `/api/project/status` | Project status updates |

## Testing

Run the test suite:

```bash
# Start the main server in one terminal
python main.py

# In another terminal, run tests
python test_agent.py
```

## Project Structure

```
mwd-agent/
├── .claude/
│   ├── mcp.json              # MCP server configuration
│   └── MCP_SETUP.md          # MCP setup and usage guide
├── docs/
│   ├── API_INTEGRATION_GUIDE.md  # AI API integration guide
│   └── conversation-history/     # Planning screenshots
├── integrations/
│   ├── gemini.py             # Gemini AI client
│   ├── openai_client.py      # OpenAI client
│   ├── perplexity.py         # Perplexity research client
│   ├── notion.py             # Notion API client
│   ├── google_workspace.py   # Google Drive/Docs client
│   ├── slack_bot.py          # Slack bot with Gemini orchestration
│   ├── slack_features.py     # Reminders, digests, quick actions
│   └── invoice_system.py     # Invoice system integration
├── main.py                   # Flask application entry point
├── test_agent.py             # Test suite
├── requirements.txt          # Python dependencies
├── MWD_AGENT_CAPABILITIES.md # Complete capabilities list
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── railway.toml              # Railway deployment config
├── PROJECT_PLAN.md           # 7-sprint project plan
└── README.md                 # This file
```

## Example Workflow: New Client Onboarding

```
1. Client fills intake form → Webhook triggers
2. Gemini receives data → Creates lead in Invoice System
3. Gemini routes to specialized AIs:
   • Claude generates branding strategy
   • Claude creates website plan
   • Claude develops social media strategy
   • Claude writes initial copy
4. Gemini orchestrates outputs:
   • Creates Notion project page
   • Organizes Google Drive folder
   • Links to Invoice System proposal
5. ChatGPT notifies team via Google Chat
6. Perplexity sends welcome to client via Slack
7. Gemini triggers invoice creation
```

## MCP (Model Context Protocol) Integration

The MWD Agent uses MCP to enable standardized multi-AI coordination and tool access.

### Available MCP Servers

**Python-based (installed via pip):**
- **Memory MCP** - Long-term memory storage for shared AI context
- **Git MCP** - Repository management and code analysis
- **Memory MCP** - Persistent storage for client context and project history

**TypeScript-based (via npx - no installation needed):**
- **Filesystem MCP** - Secure file operations for templates and assets
- **GitHub MCP** - Repository and issue management
- **PostgreSQL MCP** - Natural language database queries
- **Supabase MCP** - Supabase database integration
- **Sequential Thinking MCP** - Enhanced reasoning for complex workflows

### Configuration

MCP servers are configured in `.claude/mcp.json`. To use with Claude Desktop or VS Code:

```bash
# Claude Desktop (macOS)
cp .claude/mcp.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Claude Desktop (Linux)
cp .claude/mcp.json ~/.config/Claude/claude_desktop_config.json

# Claude Code (VS Code) - automatically detected in .claude/
```

### Usage Example

```python
from mcp import Client

# Connect to memory server for multi-AI coordination
memory_client = Client("memory")

# AI 1 (Gemini) stores meeting notes
await memory_client.call_tool("save_memory", {
    "key": "project_techflow_context",
    "value": "Client wants modern, tech-forward brand..."
})

# AI 2 (Claude) retrieves context for branding strategy
context = await memory_client.call_tool("search_memories", {
    "query": "TechFlow brand requirements"
})
```

See [.claude/MCP_SETUP.md](.claude/MCP_SETUP.md) for comprehensive setup instructions and integration patterns.

## Deployment

### Deploy to Railway (Recommended)

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and initialize**
   ```bash
   railway login
   railway init
   ```

3. **Set environment variables**
   ```bash
   railway variables set ANTHROPIC_API_KEY=your_key_here
   railway variables set GEMINI_API_KEY=your_key_here
   ```

4. **Deploy**
   ```bash
   railway up
   ```

See [PROJECT_PLAN.md](PROJECT_PLAN.md#deployment-strategy-railway) for detailed deployment instructions.

## Integration with MWD Invoice System

This agent integrates with the [MWD Invoice System](https://github.com/HouseOfVibes/mwd-invoice-system) to provide:

- Automatic lead creation from intake forms
- Project lifecycle synchronization
- Automated invoicing on deliverable completion
- Client portal integration for proposals and files

## Roadmap

### Phase 1: MVP (Complete)
- [x] Basic Flask API with 4 strategy endpoints
- [x] Claude AI integration (Sonnet 4.5)
- [x] Test suite
- [x] Latest dependencies (Nov 2025 versions)
- [x] MCP (Model Context Protocol) integration
- [x] Memory, Git, and Filesystem MCP servers
- [x] Comprehensive documentation

### Phase 2: Workspace Integration (Complete)
- [x] MCP infrastructure for multi-AI coordination
- [x] Persistent memory storage
- [x] Gemini API integration for meeting notes and orchestration
- [x] OpenAI API integration for team communication
- [x] Perplexity API integration for research and client emails
- [x] Notion API for project management and client portals
- [x] Google Workspace APIs (Drive, Docs)
- [x] Invoice System webhooks
- [x] Conversational Slack bot with Gemini orchestration
- [x] Automated reminders, digests, and quick actions
- [x] Client portal builder

### Phase 3: Advanced Intelligence (In Progress)
- [x] Multi-AI orchestration implementation
- [x] Slack bot integration with interactive components
- [ ] Agent specialization and learning
- [ ] Analytics and reporting dashboard
- [ ] Advanced MCP server integrations (GitHub, PostgreSQL)
- [ ] Google Chat integration

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete 7-sprint development roadmap.

## Cost Estimates

### AI API Costs (Monthly)
- Gemini API: $0-100 (primary workspace management)
- Claude API: $30-100 (strategic deliverables)
- ChatGPT API: $20-50 (internal communication)
- Perplexity API: $20-50 (client communication)

**Total: $70-300/month**

### Infrastructure
- Railway hosting: $5-20/month
- Supabase database: $0-25/month (free tier available)
- Node.js runtime: $0 (for TypeScript MCP servers via npx)

**Total Infrastructure + AI: $75-345/month**

## Documentation

- **[MWD_AGENT_CAPABILITIES.md](MWD_AGENT_CAPABILITIES.md)** - Complete list of everything the agent can do
- **[PROJECT_PLAN.md](PROJECT_PLAN.md)** - Comprehensive 7-sprint project plan with architecture and roadmap
- **[docs/API_INTEGRATION_GUIDE.md](docs/API_INTEGRATION_GUIDE.md)** - Complete guide for all AI API integrations with latest 2025 best practices
- **[.claude/MCP_SETUP.md](.claude/MCP_SETUP.md)** - MCP server setup, configuration, and usage guide
- **[.claude/mcp.json](.claude/mcp.json)** - MCP server configuration for Claude Desktop/Code
- **[docs/conversation-history/](docs/conversation-history/)** - Design conversation screenshots

## Contributing

This is a private project for MW Design Studio. For questions or suggestions, please open an issue.

## License

MIT License - see LICENSE file for details

## Security

- Never commit `.env` files or API keys
- All credentials stored in environment variables
- HTTPS required for production deployments
- Regular security audits planned

## Team

- **MW Design Studio** - Design and business operations
- **AI Integration** - Gemini (Google), Claude (Anthropic), ChatGPT (OpenAI), Perplexity

## Support

For issues related to:
- **Agent functionality**: Open a GitHub issue
- **Invoice System**: See [mwd-invoice-system](https://github.com/HouseOfVibes/mwd-invoice-system)
- **Business inquiries**: Contact MW Design Studio

---

**Built with ❤️ for MW Design Studio**

*Automating workflows, amplifying creativity*
