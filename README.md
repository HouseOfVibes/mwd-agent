# MWD Agent

> AI-Powered Workspace Management Agent for MW Design Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)

An intelligent multi-AI agent system that automates business workflows across branding, website design, social media strategy, copywriting, and workspace management. Integrates with Notion, Google Workspace, Slack, and the MWD Invoice System.

## 🎯 Features

- **AI-Powered Strategy Generation**: Branding, website design, social media, and copywriting deliverables
- **Workspace Intelligence**: Gemini-powered meeting notes, Notion sync, and Google Drive organization
- **Multi-AI Orchestration**: Specialized AI routing (Gemini, Claude, ChatGPT, Perplexity)
- **Invoice System Integration**: Automated lead creation, proposal generation, and client portal sync
- **Communication Hub**: Google Chat (internal) and Slack (client) integration
- **Project Management**: Automated Notion workspace updates and timeline tracking

## 🏗️ Architecture

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
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Anthropic API key (Claude)
- Google Cloud project (for Gemini API)
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

## 🔑 Environment Variables

Create a `.env` file with the following:

```bash
# Required - Current MVP
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Planned Multi-AI Integration (Phase 2)
GEMINI_API_KEY=your_gemini_api_key_here           # Primary workspace AI
OPENAI_API_KEY=your_openai_api_key_here           # Internal team communication
PERPLEXITY_API_KEY=your_perplexity_api_key_here   # Client communication & research

# Optional - Workspace Integrations
SUPABASE_URL=
SUPABASE_KEY=
SLACK_TOKEN=
NOTION_TOKEN=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Invoice System Integration
MWD_INVOICE_SYSTEM_URL=
MWD_INVOICE_SYSTEM_API_KEY=
```

### AI SDK Versions (Latest 2025)

- **Gemini**: Use `google-genai` (NEW - GA May 2025) - ⚠️ `google-generativeai` is deprecated
- **Claude**: Use `anthropic>=0.45.0` with Sonnet 4.5
- **OpenAI**: Use `openai>=1.0.0` with GPT-4o or GPT-4.1
- **Perplexity**: Use `perplexityai` with Sonar Pro model

See [docs/API_INTEGRATION_GUIDE.md](docs/API_INTEGRATION_GUIDE.md) for detailed integration instructions.

## 📡 API Endpoints

### Current Endpoints (MVP)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and service status |
| POST | `/branding` | Generate comprehensive branding strategy |
| POST | `/website` | Create website design plan and sitemap |
| POST | `/social` | Generate social media strategy |
| POST | `/copywriting` | Create marketing copy and messaging |

### Planned Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/gemini/meeting-notes` | Process Google Meet transcripts |
| POST | `/notion/sync` | Sync project to Notion workspace |
| POST | `/google/drive/organize` | Organize client folders in Drive |
| POST | `/gmail/draft` | Draft email communications |
| POST | `/slack/notify` | Send Slack notifications |
| POST | `/invoice/create-lead` | Create lead in invoice system |

## 🧪 Testing

Run the test suite:

```bash
# Start the main server in one terminal
python main.py

# In another terminal, run tests
python test_agent.py
```

## 📦 Project Structure

```
mwd-agent/
├── src/
│   ├── agents/           # Specialized AI agents
│   ├── integrations/     # External service integrations
│   ├── ai_clients/       # AI API clients (Gemini, Claude, etc.)
│   └── models/           # Data models
├── docs/
│   └── conversation-history/  # Planning screenshots
├── tests/
├── main.py              # Flask application entry point
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
├── PROJECT_PLAN.md     # Comprehensive project plan
└── README.md           # This file
```

## 🔄 Example Workflow: New Client Onboarding

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

## 🌐 Deployment

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

## 🔗 Integration with MWD Invoice System

This agent integrates with the [MWD Invoice System](https://github.com/HouseOfVibes/mwd-invoice-system) to provide:

- Automatic lead creation from intake forms
- Project lifecycle synchronization
- Automated invoicing on deliverable completion
- Client portal integration for proposals and files

## 🗺️ Roadmap

### ✅ Phase 1: MVP (Complete)
- [x] Basic Flask API with 4 strategy endpoints
- [x] Claude AI integration
- [x] Test suite

### 🔄 Phase 2: Workspace Integration (In Progress)
- [ ] Gemini API integration for meeting notes
- [ ] Notion API for project management
- [ ] Google Workspace APIs (Drive, Docs, Gmail)
- [ ] Invoice System webhooks

### 📅 Phase 3: Advanced Intelligence (Planned)
- [ ] Multi-AI orchestration (ChatGPT, Perplexity)
- [ ] Slack and Google Chat integration
- [ ] Agent specialization and learning
- [ ] Analytics and reporting dashboard

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete 7-sprint development roadmap.

## 💰 Cost Estimates

### AI API Costs (Monthly)
- Gemini API: $0-100 (primary workspace management)
- Claude API: $30-100 (strategic deliverables)
- ChatGPT API: $20-50 (internal communication)
- Perplexity API: $20-50 (client communication)

**Total: $70-300/month**

### Infrastructure
- Railway hosting: $5-20/month
- Supabase database: $0-25/month (free tier available)

## 📚 Documentation

- [PROJECT_PLAN.md](PROJECT_PLAN.md) - Comprehensive 7-sprint project plan with architecture and roadmap
- [docs/API_INTEGRATION_GUIDE.md](docs/API_INTEGRATION_GUIDE.md) - Complete guide for all AI API integrations (2025 best practices)
- [docs/conversation-history/](docs/conversation-history/) - Design conversation screenshots
- API Reference (coming soon)
- Notion Integration Guide (coming soon)

## 🤝 Contributing

This is a private project for MW Design Studio. For questions or suggestions, please open an issue.

## 📄 License

MIT License - see LICENSE file for details

## 🔒 Security

- Never commit `.env` files or API keys
- All credentials stored in environment variables
- HTTPS required for production deployments
- Regular security audits planned

## 👥 Team

- **MW Design Studio** - Design and business operations
- **AI Integration** - Gemini (Google), Claude (Anthropic), ChatGPT (OpenAI), Perplexity

## 📞 Support

For issues related to:
- **Agent functionality**: Open a GitHub issue
- **Invoice System**: See [mwd-invoice-system](https://github.com/HouseOfVibes/mwd-invoice-system)
- **Business inquiries**: Contact MW Design Studio

---

**Built with ❤️ for MW Design Studio**

*Automating workflows, amplifying creativity*
