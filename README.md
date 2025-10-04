# Matrix Project Manager Bot

A Matrix bot built with `matrix-nio` that can respond to messages.

## Features

- **Message Echo**: Responds to any message with "You said: [message]"
- **Auto-join**: Automatically accepts room invitations
- **Token Authentication**: Uses Matrix access token for secure authentication

## Setup

### 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file in the project root:

```env
MATRIX_SERVER=https://matrix.campaignlab.uk
MATRIX_BOT_USER=@github-bot:matrix.campaignlab.uk
MATRIX_ACCESS_TOKEN=your_access_token_here
```

### 3. Get Access Token

You can obtain an access token by:

**Option A: Using Element/Web**
1. Go to Settings → Help & About → Access Token
2. Copy the token to your `.env` file

**Option B: Using curl**
```bash
curl -X POST https://matrix.campaignlab.uk/_matrix/client/r0/login \
  -H "Content-Type: application/json" \
  -d '{
    "type": "m.login.password",
    "user": "github-bot",
    "password": "your_password"
  }'
```

### 4. Run the Bot

```bash
python bot.py
```

## Usage

1. Invite the bot to a Matrix room
2. Send any message in the room
3. The bot will respond with "You said: [your message]"
