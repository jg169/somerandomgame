## How to Run Synthetic_Suprises

### Quick Setup:

1. **Prerequisites:**
   - Python 3.6+ installed on your system
   - Required Python packages:
     ```
     pip install requests curses
     ```

2. **Setup Ollama:**
   - Download and install Ollama from [ollama.ai](https://ollama.ai/)
   - Ollama runs as a local server on your machine
   - After installation, pull a model using the command line:
     ```
     ollama run gemma3:4b 
     ```
     This is currently what is tested for systems with around 8gb RAM. 

   - You can also pull other models like:
     ```
     ollama run llama3:8b 
     ```

3. **Run the game:**
   - Save the code to a file named `retro_msg_board.py`
   - Run the Ollama server
   ```
   ollama serve
   ```
   This needs to be done in a separate opened terminal window


   - Run it from your terminal:
     ```
     python retro_msg_board.py
     ```

### Changing Models:

You should specify an Ollama model and a story file when starting the game:

```
python retro_msg_board.py llama3:8b starter_story.json
```


- by the way, if you get any error about like a port, restart Ollama by right clicking on its icon in the top right if you are on a mac and clicking restart ollama. 


The game will connect to your local Ollama server, which handles all the AI character responses based on the model you've selected. The more powerful the model, the more nuanced the character interactions will be!


### Optional vibe enhancers: 

- Play the start story at night with the lights off

- On your terminal, use the Homebrew theme for mac by going to shell (top left) --> New window with profile: --> select homebrew from the menu. 

- Play the background noise: [ambiance](https://www.youtube.com/watch?v=RNrVhrXrCNA) 
It helps with the vibe. 

