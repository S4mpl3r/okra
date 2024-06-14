import argparse
from threading import Thread
from time import sleep

from dotenv import load_dotenv

from okra import Assistant
from okra.utils import ConsoleManager, WavePlayer, codes

load_dotenv()

BANNER = """
    )                   
 ( /(      )            
 )\())  ( /( (       )  
((_)\   )\()))(   ( /(  
  ((_) ((_)\(()\  )(_)) 
 / _ \ | |(_)((_)((_)_  
| (_) || / /| '_|/ _` | 
 \___/ |_\_\|_|  \__,_|                         
"""

SYSTEM_PROMPT = """You are a computer assistant. Talk to the user about anything that they want.
Be as precise and brief as possible.
Avoid using emojis or anything of that sort in your response.
Be friendly, polite and casual, like a close friend. Try not to be a creep though.
Your response will be given to a text-to-speech model, so optimize for spoken text.
**Optional**
You will sometimes be given an image too, this image will either be a screenshot of the user's computer screen, or an image captured from their webcam.
By default, do not comment on the image, unless the user asks a question about it. Only then you can use this image to answer user's question
"""


def play_intro_music():
    music_thread = WavePlayer(
        "./assets/audio/AI Assistant Intro_01.wav",
        daemon=True,
        name="Music Player Thread",
    )
    music_thread.start()
    return music_thread


def intro(skip_music: bool = False):
    if not skip_music:
        music_thread = play_intro_music()

    console = ConsoleManager.console()
    console.control(codes["HIDE_CURSOR"])
    console.print(BANNER, style="bright_green")
    for i in range(10):
        console.print("[green].[/green]", end=" ")
        sleep(0.3)
    console.print("[green].[/green]", end="")
    console.control(codes["ERASE_LINE"], codes["CARRIAGE_RETURN"])
    for i in [*"Welcome to Okra, your all in one AI companion!"]:
        console.print(i, end="")
        sleep(0.1)
    sleep(0.5)
    console.control(codes["ERASE_LINE"], codes["CARRIAGE_RETURN"])
    console.print(
        "Welcome to [bright_green]Okra[/bright_green], your all in one [purple3]AI[/purple3] companion!"
    )
    sleep(2)

    try:
        console.print("→ Press enter to continue...", highlight=False, end="")
        input()
    except:
        return

    console.control(codes["ERASE_LINE"])
    console.control(codes["CURSOR_UP"])
    console.control(codes["ERASE_LINE"])
    console.control(codes["CARRIAGE_RETURN"])

    if not skip_music:
        music_thread.stop()
        music_thread.join()

    console.control(codes["ERASE_LINE"])
    console.control(codes["CARRIAGE_RETURN"])


def main(skip_intro: bool = False, skip_music: bool = False):
    if skip_intro:
        a = Assistant(system_prompt=SYSTEM_PROMPT)
        a.chat()
        return

    try:
        intro_thread = Thread(
            name="Intro Thread", target=intro, args=(skip_music,), daemon=True
        )
        intro_thread.start()

        a = Assistant(system_prompt=SYSTEM_PROMPT)

        while intro_thread.is_alive():
            intro_thread.join(1)

        a.chat()
    except KeyboardInterrupt:
        print("\nCtrl+C")
    except Exception as e:
        print("Exiting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Okra is your all in one desktop AI voice assistant.",
        usage="python okra.py [options]",
    )

    parser.add_argument("--skip-intro", action="store_true", help="skip intro")
    parser.add_argument(
        "--no-music", action="store_true", help="do not play intro music"
    )

    args = parser.parse_args()

    if args.skip_intro:
        main(skip_intro=True)
    elif args.no_music:
        main(skip_music=True)
    else:
        main()
