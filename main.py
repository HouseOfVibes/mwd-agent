#!/usr/bin/env python3
"""
MWD Agent - Marketing Website Design Agent
Handles branding, website design, social media, and copywriting workflows
"""

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Anthropic client
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Configuration check
def check_config():
    """Check which services are configured"""
    config_status = {
        'anthropic': '✅ Configured' if os.getenv('ANTHROPIC_API_KEY') else '❌ Missing',
        'supabase': '✅ Configured' if os.getenv('SUPABASE_URL') else '⚠️  Optional',
        'slack': '✅ Configured' if os.getenv('SLACK_TOKEN') else '⚠️  Optional'
    }
    return config_status

# Agent prompts
BRANDING_PROMPT = """You are a branding expert helping create a comprehensive brand identity.

Based on the client information provided, create:
1. Brand positioning statement
2. Target audience definition
3. Brand personality (3-5 traits)
4. Color palette suggestions (primary, secondary, accent colors)
5. Typography recommendations
6. Key messaging points

Client Info:
{client_info}

Return your response as a structured JSON object."""

WEBSITE_PROMPT = """You are a website design strategist creating a website plan.

Based on the client information and branding, create:
1. Sitemap (main pages and structure)
2. Homepage layout description
3. Key page descriptions
4. Call-to-action strategy
5. User journey map

Client Info:
{client_info}

Return your response as a structured JSON object."""

SOCIAL_PROMPT = """You are a social media strategist creating a content plan.

Based on the client information and branding, create:
1. Platform recommendations (which social media platforms and why)
2. Content pillars (3-5 main themes)
3. Posting frequency recommendations
4. Sample post ideas (5 examples)
5. Hashtag strategy

Client Info:
{client_info}

Return your response as a structured JSON object."""

COPYWRITING_PROMPT = """You are a professional copywriter creating marketing copy.

Based on the client information and branding, create:
1. Tagline options (3-5 variations)
2. About section copy
3. Value proposition statement
4. Service/Product descriptions
5. Email welcome sequence outline

Client Info:
{client_info}

Return your response as a structured JSON object."""


def call_claude(prompt, client_data):
    """Call Claude API with the given prompt and client data using latest features"""
    try:
        formatted_prompt = prompt.format(client_info=str(client_data))

        message = anthropic_client.messages.create(
            model="claude-sonnet-4-5-20250929",  # Latest Sonnet 4.5 model
            max_tokens=4096,
            messages=[
                {"role": "user", "content": formatted_prompt}
            ],
            # Enable prompt caching for repeated system prompts (future enhancement)
            # system=[
            #     {
            #         "type": "text",
            #         "text": "System instructions here",
            #         "cache_control": {"type": "ephemeral"}
            #     }
            # ]
        )

        return {
            'success': True,
            'response': message.content[0].text,
            'usage': {
                'input_tokens': message.usage.input_tokens,
                'output_tokens': message.usage.output_tokens,
                'cache_creation_tokens': getattr(message.usage, 'cache_creation_input_tokens', 0),
                'cache_read_tokens': getattr(message.usage, 'cache_read_input_tokens', 0)
            }
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@app.route('/')
def home():
    """Health check and service status"""
    config = check_config()
    return jsonify({
        'status': 'running',
        'service': 'MWD Agent',
        'config': config,
        'endpoints': [
            '/branding',
            '/website',
            '/social',
            '/copywriting'
        ]
    })


@app.route('/branding', methods=['POST'])
def branding():
    """Generate branding strategy"""
    client_data = request.json
    result = call_claude(BRANDING_PROMPT, client_data)
    return jsonify(result)


@app.route('/website', methods=['POST'])
def website():
    """Generate website design plan"""
    client_data = request.json
    result = call_claude(WEBSITE_PROMPT, client_data)
    return jsonify(result)


@app.route('/social', methods=['POST'])
def social():
    """Generate social media strategy"""
    client_data = request.json
    result = call_claude(SOCIAL_PROMPT, client_data)
    return jsonify(result)


@app.route('/copywriting', methods=['POST'])
def copywriting():
    """Generate marketing copy"""
    client_data = request.json
    result = call_claude(COPYWRITING_PROMPT, client_data)
    return jsonify(result)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 MWD Agent starting on port 8080")
    print("="*50)

    config = check_config()
    print("\n📋 Configuration Status:")
    print(f"  Anthropic API: {config['anthropic']}")
    print(f"  Supabase: {config['supabase']}")
    print(f"  Slack: {config['slack']}")

    print("\n🔗 Endpoints available:")
    print("  POST /branding")
    print("  POST /website")
    print("  POST /social")
    print("  POST /copywriting")
    print("\n" + "="*50 + "\n")

    app.run(host='0.0.0.0', port=8080, debug=True)
