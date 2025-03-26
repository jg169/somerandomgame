#!/usr/bin/env python3
"""
RetroNet BBS: Simplified Terminal-Based BBS Simulation
Loads characters and story from a JSON file and simulates a BBS chatroom.
"""

import os
import sys
import time
import random
import json
import requests
import argparse
from typing import Dict, List, Any

class RetroNetBBS:
    """Simple BBS simulation that loads content from a JSON file"""
    
    def __init__(self, story_file: str, model: str = "mistral"):
        self.player_name = ""
        self.message_history = []
        self.time = "19:45"
        self.connected_users = []
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = model
        
        # Load story data from JSON file
        self.load_story(story_file)
    
    def load_story(self, story_file: str):
        """Load story content from a JSON file"""
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract characters
            self.characters = {char["username"]: char for char in data["characters"]}
            
            # Extract story title if available
            self.story_title = data.get("title", "RetroNet BBS")
            
            # Date from story if provided
            if all(key in data for key in ["year", "month", "day"]):
                self.story_date = f"{data['month']}/{data['day']}/{data['year']}"
            else:
                self.story_date = "2/28/1995"  # Default date
                
            print(f"Successfully loaded story: {self.story_title}")
            
        except Exception as e:
            print(f"Error loading story file: {e}")
            sys.exit(1)
    
    def run_game(self):
        """Main game function that handles setup and main loop"""
        # Show welcome banner
        print("\033[92m" + """
 ██████╗░███████╗████████╗██████╗░░█████╗░███╗░░██╗███████╗████████╗
 ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗████╗░██║██╔════╝╚══██╔══╝
 ██████╔╝█████╗░░░░░██║░░░██████╔╝██║░░██║██╔██╗██║█████╗░░░░░██║░░░
 ██╔══██╗██╔══╝░░░░░██║░░░██╔══██╗██║░░██║██║╚████║██╔══╝░░░░░██║░░░
 ██║░░██║███████╗░░░██║░░░██║░░██║╚█████╔╝██║░╚███║███████╗░░░██║░░░
 ╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝╚══════╝░░░╚═╝░░░
                          Terminal
          """ + "\033[0m")
        
        # Show story title
        print(f"\033[93m\n{self.story_title.upper()}\033[0m")
        
        # Connecting animation
        print("\033[93m" + "CONNECTING AT 14.4kbps...\n" + "\033[0m")
        self._simulate_connecting()
        
        # Get username
        print("\033[93m" + f"\nWelcome to RetroNet BBS - Est. 1992" + "\033[0m")
        print("SysOp: Please enter your username to connect")
        
        while not self.player_name:
            name = input("> ").strip()
            if name and name not in self.characters:
                self.player_name = name
            else:
                print("SysOp: That username is already taken or invalid. Please try another.")
        
        print(f"\nSysOp: Welcome, {self.player_name}! You are now connected to RetroNet BBS.")
        print("SysOp: Type 'help' to see available commands.\n")
        
        # Initialize starting characters - pick some random ones
        self.connected_users = []
        if "SysOp" in self.characters:
            self.connected_users.append("SysOp")
            
        # Add 2 random characters if available
        other_chars = [u for u in self.characters.keys() if u != "SysOp"]
        if other_chars:
            initial_chars = random.sample(other_chars, min(2, len(other_chars)))
            self.connected_users.extend(initial_chars)
        
        # Add welcome messages
        self.message_history.append({
            "user": "SysOp" if "SysOp" in self.characters else "SYSTEM",
            "message": f"Welcome to RetroNet BBS, {self.player_name}! Current users: {len(self.connected_users) + 1}",
            "timestamp": self.time
        })
        
        # Add initial messages from connected characters
        for user in self.connected_users:
            if user != "SysOp":
                welcome_messages = [
                    f"hey {self.player_name}! new to this board?",
                    f"welcome to the underground, {self.player_name}",
                    f"sup {self.player_name}, where u calling in from?",
                    f"another new user? cool. i'm {user}",
                    f"hey {self.player_name}, good to see fresh blood around here"
                ]
                self.message_history.append({
                    "user": user,
                    "message": random.choice(welcome_messages),
                    "timestamp": self.time
                })
        
        # Show initial messages
        self._show_recent_messages(10)
        
        # Main game loop
        running = True
        while running:
            try:
                command = input(f"\033[92m{self.player_name}>\033[0m ")
                running = self._process_command(command)
                
                # Advance time with each command
                self._advance_time()
                
                # Random chance for character activity
                if random.random() < 0.4:
                    self._random_character_activity()
                
            except KeyboardInterrupt:
                print("\nDisconnecting from RetroNet BBS...")
                running = False
            except Exception as e:
                print(f"ERROR: {str(e)}")
        
        print("\nThank you for using RetroNet BBS. Goodbye!")
    
    def _simulate_connecting(self):
        """Visual effect for connecting to the BBS"""
        connecting_steps = [
            "Dialing...",
            "CARRIER DETECTED...",
            "NEGOTIATING PROTOCOL...",
            "CONNECTED at 14400 bps..."
        ]
        
        for step in connecting_steps:
            print(step)
            time.sleep(0.5)  # Fast connection simulation
    
    def _advance_time(self):
        """Advance the in-game time"""
        hour, minute = map(int, self.time.split(':'))
        minute += 5
        
        if minute >= 60:
            hour += minute // 60
            minute = minute % 60
            
        if hour >= 24:
            hour = hour % 24
        
        self.time = f"{hour:02d}:{minute:02d}"
        
        # Special midnight event - chance for rarer character to join
        if self.time == "00:00" and random.random() < 0.3:
            self._midnight_event()
    
    def _midnight_event(self):
        """Event that happens at midnight"""
        # Try to bring in a character who isn't already online
        offline_chars = [u for u in self.characters.keys() if u not in self.connected_users]
        if offline_chars:
            new_char = random.choice(offline_chars)
            self.connected_users.append(new_char)
            
            self.message_history.append({
                "user": "SysOp" if "SysOp" in self.characters else "SYSTEM",
                "message": f"{new_char} has joined the chat",
                "timestamp": self.time
            })
            
            # Special midnight message
            midnight_messages = [
                "the night shift has arrived",
                "midnight. interesting things happen at this hour.",
                "who else is up late? can't sleep...",
                "midnight crew checking in"
            ]
            
            self.message_history.append({
                "user": new_char,
                "message": random.choice(midnight_messages),
                "timestamp": self.time
            })
            
            # Show the messages
            self._show_recent_messages(2)
    
    def _random_character_activity(self):
        """Generate random character activity"""
        # Random chance of users joining/leaving
        if random.random() < 0.9:
            self._user_join_leave()
        
        # Random chance of idle message
        if random.random() < 0.3:
            self._generate_idle_message()
    
    def _user_join_leave(self):
        """Random users join or leave the chat"""
        all_usernames = list(self.characters.keys())
        online_users = self.connected_users.copy()
        offline_users = [u for u in all_usernames if u not in online_users]
        
        # Someone joins
        if len(offline_users) > 0 and random.random() < 0.8:
            user_to_join = random.choice(offline_users)
            self.connected_users.append(user_to_join)
            
            self.message_history.append({
                "user": "SysOp" if "SysOp" in self.characters else "SYSTEM",
                "message": f"{user_to_join} has joined the chat",
                "timestamp": self.time
            })
            
            # Entry message
            entry_message = f"hey everyone. {random.choice(['just logged in', 'what did i miss?', 'anyone here?', 'how\'s it going?'])}"
            
            self.message_history.append({
                "user": user_to_join,
                "message": entry_message,
                "timestamp": self.time
            })
            
            # Show join messages
            self._show_recent_messages(2)
        
        # Someone leaves
        elif len(online_users) > 0 and random.random() < 0.2:
            # Don't let SysOp leave if they're a character
            if "SysOp" in online_users and len(online_users) > 1:
                online_users.remove("SysOp")
                
            user_to_leave = random.choice(online_users)
            self.connected_users.remove(user_to_leave)
            
            self.message_history.append({
                "user": "SysOp" if "SysOp" in self.characters else "SYSTEM",
                "message": f"{user_to_leave} has left the chat",
                "timestamp": self.time
            })
            
            # Show leave message
            self._show_recent_messages(1)
    
    def _generate_idle_message(self):
        """Generate random idle message from a character"""
        if not self.connected_users:
            return
            
        user = random.choice(self.connected_users)
        character = self.characters[user]
        
        # Use idle messages if available
        if "idle_messages" in character and isinstance(character["idle_messages"], list) and len(character["idle_messages"]) > 0:
            message = random.choice(character["idle_messages"])
        else:
            message = f"just hanging out on the board"
        
        # Add message to history
        self.message_history.append({
            "user": user,
            "message": message,
            "timestamp": self.time
        })
        
        # Show the new message
        self._show_recent_messages(1)
    
    def _process_command(self, command):
        """Process user commands"""
        parts = command.strip().split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Process commands
        if cmd == "help":
            self._show_help()
        elif cmd == "users":
            self._show_users()
        elif cmd == "say":
            self._send_message(args)
        elif cmd == "time":
            print(f"Current BBS time: {self.time}")
            print(f"Date: {self.story_date}")
        elif cmd == "refresh":
            self._show_recent_messages(15)
        elif cmd == "who":
            self._show_character_info(args)
        elif cmd == "quit" or cmd == "exit":
            return False
        else:
            # Treat as message
            self._send_message(command)
        
        return True
    
    def _show_help(self):
        """Display available commands"""
        print("\n\033[93mAvailable commands:\033[0m")
        print("  help       - Show this help message")
        print("  users      - Show users currently online")
        print("  say [msg]  - Send a message (or just type the message)")
        print("  who [user] - Show information about a user")
        print("  time       - Show current BBS time")
        print("  refresh    - Show recent messages")
        print("  quit       - Disconnect from BBS\n")
    
    def _show_users(self):
        """Show users currently online"""
        print("\n\033[93mUsers currently online:\033[0m")
        print(f"  {self.player_name} (You)")
        for user in self.connected_users:
            print(f"  {user}")
        print("")
    
    def _show_character_info(self, username):
        """Show information about a character"""
        if not username:
            print("Usage: who [username]")
            return
            
        if username not in self.characters:
            print(f"No user named '{username}' found.")
            return
            
        char = self.characters[username]
        print(f"\n\033[93mUser Profile: {char['username']}\033[0m")
        print(f"Description: {char['description']}")
        
        if "specialty" in char:
            print(f"Specialty: {char['specialty']}")
            
        print("")
    
    def _send_message(self, message):
        """Send a message to the chat"""
        if not message.strip():
            return
            
        # Log player message
        self.message_history.append({
            "user": self.player_name,
            "message": message,
            "timestamp": self.time
        })
        
        # Character responses - 1-2 characters might respond
        character_responses = 0
        for char_name in self.connected_users:
            # Each character has a chance to respond
            if random.random() < 0.4 and character_responses < 2:  # Limit to 2 responses
                character_responses += 1
                
                # Use Ollama to generate response if available, otherwise use fallback
                try:
                    response = self._generate_character_response(char_name, message)
                except:
                    # Fallback if Ollama is not available
                    character = self.characters[char_name]
                    fallback_responses = [
                        f"interesting point about {message[:10]}...",
                        "hmm, not sure what to think about that",
                        "i've been wondering about that too",
                        "anyone else have thoughts on this?",
                        f"that reminds me of something i saw on another board"
                    ]
                    response = random.choice(fallback_responses)
                
                # Log character response
                self.message_history.append({
                    "user": char_name,
                    "message": response,
                    "timestamp": self.time
                })
        
        # Show the messages
        self._show_recent_messages(2 + character_responses)
    
    def _generate_character_response(self, character_name, prompt):
        """Generate a response from a character using Ollama"""
        character = self.characters[character_name]
        
        # Ollama prompt
        system_prompt = f"""
        You are roleplaying as {character_name}, a user in a 1990s BBS chatroom.
        
        Character details:
        - Username: {character['username']}
        - Description: {character['description']}
        - Personality: {character['personality'] if 'personality' in character else 'Friendly and helpful'}
        
        Current date: {self.story_date}
        
        Format your responses as if typing in a 90s chatroom:
        - Use lowercase mostly
        - Use period-appropriate 90s slang and references
        - Keep responses relatively brief (1-3 sentences)
        - Sometimes use chat shorthand like "brb", "lol", "afk"
        - Refer to technical things like "the web", "modems", "bbs", etc.
        
        The user is asking: "{prompt}"

        ## The state of the chatroom is: {self.message_history[-10:]}
        
        Respond as {character_name}:
        """
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": system_prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "ERROR: No response generated")
            else:
                return f"ERROR: Failed to generate response (Status code: {response.status_code})"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def _show_recent_messages(self, count=10):
        """Display recent messages"""
        print("\n\033[93m--- Recent Messages ---\033[0m")
        
        # Get recent messages
        recent = self.message_history[-count:] if len(self.message_history) > count else self.message_history
        
        for msg in recent:
            user = msg["user"]
            message = msg["message"]
            timestamp = msg["timestamp"]
            
            # Color code by user
            if user == "SysOp" or user == "SYSTEM":
                print(f"\033[93m[{timestamp}] {user}: {message}\033[0m")
            elif user == self.player_name:
                print(f"\033[92m[{timestamp}] {user}: {message}\033[0m")
            else:
                print(f"\033[96m[{timestamp}] {user}: {message}\033[0m")
        print("")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="RetroNet BBS: Terminal Chatroom")
    parser.add_argument("model", nargs="?", default="mistral", help="Ollama model to use (default: mistral)")
    parser.add_argument("story_file", nargs="?", default="retronet_story.json", 
                       help="Path to the story JSON file (default: retronet_story.json)")
    parser.add_argument("--ollama-url", default="http://localhost:11434/api/generate", 
                       help="Ollama API URL (default: http://localhost:11434/api/generate)")
    args = parser.parse_args()
    
    # Check if story file exists
    if not os.path.exists(args.story_file):
        print(f"Error: Story file '{args.story_file}' not found.")
        print(f"Please create a story file or specify an existing one.")
        return 1
    
    # Create and run the game
    try:
        game = RetroNetBBS(args.story_file, args.model)
        game.ollama_url = args.ollama_url
        game.run_game()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())