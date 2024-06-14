# Okra
![screenshot](https://github.com/S4mpl3r/okra/blob/main/assets/images/screenshot2.jpg)

> Some love it, some hate it, others don't even know that it exists, just like the real-life okra!

Okra is your all-in-one personal AI assistant. This is my effort at recreating something similar to ChatGPT's desktop application. Even though it has a LOT of room for improvement, it's still pretty fun to play with.


## Features
- **Speech recognition:** Okra listens to you in the background and recognizes your speech, using the power of the well-known [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library.
- **Speech-to-text conversion:** Okra uses external speech-to-text APIs to transcribe your speech. The currently supported speech-to-text providers are:
   - [Deepgram](https://deepgram.com)
   - [Groq](https://groq.com)
   - [OpenAI](https://openai.com)
- **Vision capabilities:** You can share your webcam feed **or** your computer screen with okra, and it will use the image to chat with you and answer your questions!
- **Multiple LLM support:** Okra supports multiple LLM and VLM API providers. The currently available providers are:
   - [Google (Gemini)](https://aistudio.google.com/)
   - [OpenAI (GPT)](https://platform.openai.com/)
   - [Groq (Llama3, Gemma, Mixtral-8x7b)](https://console.groq.com/)
- **Text-to-speech capability:** Okra can speak to you, using various text-to-speech models. Currently, it supports:
   - [Deepgram](https://deepgram.com)
   - [OpenAI](https://openai.com)

## Installation
To install, do the following:
1. Clone the repository:
   ```bash
   git clone https://github.com/S4mpl3r/okra.git
   ```
2. Create a python environment and activate it. (optional, but highly recommended)
   ```bash
   # Windows
   python -m venv .venv
   .venv/Scripts/activate
   # Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Create a `.env` file in the project root and populate it with your API keys according to the `.env.example` file provided:
   ```bash
   DEEPGRAM_API_KEY=
   GROQ_API_KEY=
   GOOGLE_API_KEY=
   OPENAI_API_KEY=
   ```
3. Install the required packages
   ```bash
   # Windows
   python -m pip install -r requirements.txt
   # Linux
   python3 -m pip install -r requirements.txt
   ```
4. Edit the `okra/config.py` file to your liking. The default configuration uses `gemini-1.5-flash` as the llm, `groq` as the speech-to-text provider, and `deepgram` as the text-to-speech provider:
   ```python
   # okra/config.py
   config: GlobalConfig = {
        # Make this False if you don't want to use vision,
        # or the model that you use does not support it
        "use_vision": True,
        # Make this False if you don't want okra to generate speech
        "talk": True,
        # The source of vision, can be either 'screen' (your computer screen) or 'webcam' 
        "image_source": "screen",
        # The llm to use
        "llm": Gemini(
            model_name="models/gemini-1.5-flash-latest",
            system_prompt=system_prompt,
            max_history_length=10,
        ),
        # The speech-to-text model to use
        "speech_to_text": GroqSpeechToText(),
        # The text-to-speech model to use
        "text_to_speech": DeepgramTextToSpeech(),
    }
   ```
5. Run the tool:
   ```bash
   # Windows
   python okra.py
   # Linux
   python3 okra.py
   ```

## Options
You can edit the `okra/config.py` file to change the behavior of okra to your liking. You have access to:
- 3 LLM classes found in `okra.llm` subpackage:
   - `Gemini`
   - `GPT`
   - `GroqLLM`
- 3 speech-to-text classes found in `okra.speech` subpackage:
   - `DeepgramSpeechToText`
   - `OpenAISpeechToText`
   - `GroqSpeechToText`
- 2 text-to-speech classes found in `okra.speech` subpackage:
   - `DeepgramTextToSpeech`
   - `OpenAITextToSpeech`
### Example config 1
- LLM: OpenAI
- Speech-to-text: Deepgram
- Text-to-speech: Deepgram
- Vision source: screen
```python
# okra/config.py
config: GlobalConfig = {
    "use_vision": True,
    "talk": True,
    "image_source": "screen",
    "llm": GPT(
        model_name="gpt-4o",
        system_prompt=system_prompt,
        max_history_length=10,
    ),
    "speech_to_text": DeepgramSpeechToText(),
    "text_to_speech": DeepgramTextToSpeech(),
}
```
### Example config 2
- LLM: Groq
- Speech-to-text: Deepgram
- Text-to-speech: OpenAI
- No vision
```python
# okra/config.py
config: GlobalConfig = {
    "use_vision": False, # Groq does not support vision models (yet)
    "talk": True,
    "image_source": "screen",
    "llm": GroqLLM(
        model_name="llama3-70b-8192",
        system_prompt=system_prompt,
        max_history_length=10,
    ),
    "speech_to_text": DeepgramSpeechToText(),
    "text_to_speech": OpenAITextToSpeech(),
}
```
## Usage
If you run `python okra.py -h`, you'll get:
```bash
usage: python okra.py [options]

Okra is your all in one desktop AI voice assistant.

options:
  -h, --help    show this help message and exit
  --skip-intro  skip intro
  --no-music    do not play intro music
```
By default, okra will play an intro cutscene and music [^1] (just for fun, lol). If you want to skip this intro, run `python okra.py --skip-intro`. If you just want to mute the music, run `python okra.py --no-music`. 

To exit the assistant, type 'q' and press enter in the terminal.

Have fun!

## License
MIT

[^1]: The intro music was created with [Suno](https://suno.ai/)