"""
Matrix Project Manager Bot

A simple Matrix bot that can be used for project management tasks.
The bot automatically joins rooms it's invited to and responds to messages.

Dependencies:
- python-nio: Matrix client library
- python-dotenv: Environment variable management
"""

import asyncio
import os
from dotenv import load_dotenv
from nio import AsyncClient, MatrixRoom, RoomMessageText, InviteEvent

load_dotenv()
MATRIX_SERVER = os.getenv(
    "MATRIX_SERVER"
)
MATRIX_BOT_USER = os.getenv(
    "MATRIX_BOT_USER"
)
MATRIX_ACCESS_TOKEN = os.getenv(
    "MATRIX_ACCESS_TOKEN"
)

class MatrixTestBot:
    """
    A Matrix bot that handles project management tasks.

    This bot can:
    - Automatically join rooms when invited
    - Respond to text messages in rooms
    - Echo back messages for testing purposes
    """

    def __init__(self):
        """
        Initialize the Matrix bot client and set up event handlers.

        Creates an AsyncClient instance and registers callback functions
        for different types of Matrix events.
        """
        # Create the Matrix client instance
        # This will connect to the specified Matrix homeserver
        self.client = AsyncClient(MATRIX_SERVER, MATRIX_BOT_USER)

        # Store the bot's user ID for reference
        # Used to identify messages sent by the bot itself
        self.bot_user_id = MATRIX_BOT_USER

        # Register event callbacks - these functions will be called when events occur
        # RoomMessageText: Triggered when someone sends a text message in a room
        self.client.add_event_callback(self.message_callback, RoomMessageText)

        # InviteEvent: Triggered when the bot receives a room invitation
        self.client.add_event_callback(self.invite_callback, InviteEvent)

    async def login(self):
        """
        Authenticate with the Matrix homeserver using an access token.

        This method sets up the authentication credentials and verifies
        that the token is valid by making a test API call.

        Returns:
            The response from the whoami API call if successful

        Raises:
            Exception: If the access token is invalid or authentication fails
        """
        print(f"Using access token for user: {MATRIX_BOT_USER}")
        print(f"Server: {MATRIX_SERVER}")

        # Set the access token directly on the client
        # This bypasses the normal login flow since we already have a token
        self.client.access_token = MATRIX_ACCESS_TOKEN
        self.client.user_id = MATRIX_BOT_USER

        # Verify the token works by making a simple API request
        # The whoami endpoint returns information about the authenticated user
        response = await self.client.whoami()

        # Check if the response contains a user_id, indicating successful authentication
        if hasattr(response, "user_id"):
            print(f"Successfully authenticated as {response.user_id}")
            return response
        else:
            # If no user_id in response, the token is invalid
            raise Exception(f"Token authentication failed: {response}")

    async def invite_callback(self, room: MatrixRoom, event: InviteEvent):
        """
        Automatically accept room invitations.

        This callback is triggered whenever the bot receives an invitation
        to join a Matrix room. The bot will automatically accept all invitations.

        Args:
            room (MatrixRoom): The room object containing room information
            event (InviteEvent): The invitation event details
        """
        print(f"Received invite to {room.room_id}")

        # Automatically join the room
        # This makes the bot available in any room it's invited to
        await self.client.join(room.room_id)
        print(f"Joined room {room.room_id}")

    async def message_callback(self, room: MatrixRoom, event: RoomMessageText):
        """
        Handle incoming text messages in Matrix rooms.

        This callback is triggered whenever someone sends a text message
        in a room where the bot is present. Currently, the bot echoes back
        the message with a prefix for testing purposes.

        Args:
            room (MatrixRoom): The room where the message was sent
            event (RoomMessageText): The message event containing the text content
        """
        # Ignore messages from the bot itself to prevent infinite loops
        if event.sender == self.bot_user_id:
            return

        # Log the received message for debugging purposes
        print(f"Received message in {room.room_id}")
        print(f"From: {event.sender}")
        print(f"Message: {event.body}")

        # Send a reply message back to the room
        # @todo update functionality - currently echo's back the message
        await self.client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": f"You said: {event.body}",
            },
        )
        print("Sent reply")

    async def start(self):
        """
        Start the Matrix bot and begin listening for events.

        This method handles the complete bot startup process:
        1. Authenticate with the Matrix server
        2. Perform initial sync to get current state
        3. Begin continuous syncing to receive real-time events

        The bot will run indefinitely until stopped by the user or an error occurs.
        """
        print(f"Starting bot as {self.bot_user_id}")
        print("Connecting to Matrix server...")

        # Step 1: Authenticate with the Matrix server
        await self.login()

        # Step 2: Perform initial sync to get the current state
        # This downloads all recent events and room information
        # Timeout is set to 30 seconds (30000ms)
        await self.client.sync(timeout=30000)
        print("Initial sync complete. Bot is now running...")
        print("Send any message in a room with the bot to test!")

        # Step 3: Keep syncing forever to receive real-time events
        # full_state=True ensures we get complete room state on each sync
        await self.client.sync_forever(timeout=30000, full_state=True)


async def main():
    """
    Main entry point for the bot application.

    Creates a bot instance and starts it running.
    This function is used when the script is imported as a module.
    """
    bot = MatrixTestBot()
    await bot.start()


if __name__ == "__main__":
    """
    Entry point when the script is run directly.

    This block handles the main execution flow and provides
    proper error handling for common scenarios like user interruption
    or unexpected crashes.
    """
    # Create a new bot instance
    bot = MatrixTestBot()

    try:
        # Run the bot using asyncio
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Bot crashed: {e}")