# About our AI Pathfinder Companion
This project was made with the collaborative effort of Jhun Baclaan, Noel Ah Mook Sang, and Adriane Fiesta.

The application is our submission for the 2025 Hawaii Annual Code Challenge (HACC). The specific challenge is Challenge 4: *University of Hawaii (UH) – UH Pathfinder AI – Discover My Educational Pathway*, authored by Garret Yoshimi.
# Concept and Features
Our pathfinder companion is housed within a webpage built using HTML/CSS, Python, and Javascript via Django. The AI companion uses Gemini 2.5 Flash Lite as its model, which uses a CSV made from UH Manoa's 2024-2025 catalog to build its responses. The AI was given multiple context strings to refine and create concise responses, as well as to handle edge cases. This way, users can learn about their possible course plan without having the response feel *too* much like it's made by AI.

The AI will always generate a four-year course plan; this course plan orders courses for a typical four-year degree (e.g. ICS 100 first, then ICS 200), however it does not factor in pre-requisites. On top of this, if a user doesn't exactly know what they want to major in, the AI is able to ask about the user's interests and generate a few majors which can allow a user to explore potential course pathways.
# Installation and Use
## Precaution -- API Key
Using this application requires you to have a Google AI Studio API key. This api key should be stored in a *.env* in the line
```
GEMINI_API_KEY=[insert api key here]
```
**We recommend that you use your own API key for your own usage of this application; there are security concerns revolving around using other people's API keys. If you do require an API key but do not know how to make one, contact Jhun Baclaan either through Slack DMs or via email @lainiwajp@gmail.com.**

The installation and use of our pathfinder companion assumes that you have **basic** knowledge of
your system's Command Line/Terminal. **It also assumes that you have the latest version of python (in some cases, python3.11; see 'Troubleshooting') installed
on your system. If you do not have it installed, find their releases page [here](https://www.python.org/downloads/).**

The latest release can be downloaded from code -> download ZIP. Download it and unpack in a place that you can easily access.

After unpacking the .zip, navigate to its directory on your Command Line with 'cd'. Once you're at the base directory,
use the following command:
```
source venv/bin/activate
```
This will activate the venv, and allow you to run the app.

Running the application is equally as easy. After activating the venv, run the server with:
```
python manage.py runserver
```
Your command line will return a line along the lines of `Starting development server at...` alongside a URL. 
This URL can be copied and pasted into any browser to access TaskMaster. From here, you can add and manage your tasks as you'd like.
# Troubleshooting
## Python
During development, we did run into a few issues with how the versions of certain modules are linked to the versions of Python being used. This created problems with programming the backend of the AI, as some versions would use deprecated functions that would prevent compatibility with using any Gemini model.
Because of this, the venv used for housing all of the app's modules and necessary python files were made with python3.11. Using older versions of Python will cause the venv to refuse to load.

If you are encountering issues like this, please upgrade to python3.11. We have also found that later versions of python also work -- so if you use something like the latest release of Python (v.3.14), you're completely fine.
