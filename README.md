# Dialogflow Helper

## What is this for?

Automatically creating an agent zip file for importing into dialogflow from CSVs.

## Quick usage
```
# Example use:
python3 agent-helper --intents intents.csv --phrases phrases.csv -V 1.0.1 -z 
```

```
python3 agent-helper/ -h
usage:  [-h] [--name [NAME]] [--intents [INTENTS]] [--phrases [PHRASES]]
        [-o [OUTPUT]] [-z] [-V VERSION]

Generate DialogFlow Agents from CSV files!

optional arguments:
  -h, --help            show this help message and exit
  --name [NAME]         Name of agent (Default: agent)
  --intents [INTENTS]   Select csv file to generate intent responses from.
  --phrases [PHRASES]   Select csv file to generate training phrases from.
  -o [OUTPUT], --output [OUTPUT]
                        Name of output zip. (without .zip at the end)
  -z, --zip             Create zip file automatically.
  -V VERSION, --version VERSION
                        Set a version (Default: 1.0.0)

```

## CSV file format

### Intents

```
    python3 agent-helper --intents <csv filepath>
```

For example, an intents csv file may look like this:

| intent                  | response1               | response2          | response3 | ... | responseX |
| ----------------------- | ----------------------- | ------------------ | --------- | --- | --------- |
| smalltalk.agent.neutral | hello                   | hi                 | greetings |     |           |
| smalltalk.agent.neutral | Great weather isn't it? |                    |           |     |           |
| smalltalk.agent.neutral | Nice chat!              | What a lovely day! |           |     |           |
| smalltalk.agent.bad     | Thanks for nothing!     | Go away!           |           |     |           |
| smalltalk.agent.bad     | BYE!                    |                    |           |     |           |

The bot may respond for the `smalltalk.agent.neutral` intent as:

- hello
- Great weather isn't it?
- Nice chat!

As 3 separate speech bubbles/messages.

Adding more `response` columns provides the bot with variants for the same message. For example, the bot may respond with EITHER "hello", "hi" or "greetings" for its first message.

Each row represents a message sent by the bot in response to the intent.
Multiple rows results in multiple text bubbles sent by the bot.

### Training Phrases

```
    python3 agent-helper --phrases <csv filepath>
```

For example, an phrase csv file may look like this:

| intent                  | phrase       |
| ----------------------- | ------------ |
| smalltalk.agent.neutral | hi           |
| smalltalk.agent.neutral | what's up    |
| smalltalk.agent.neutral | how are you! |
| smalltalk.agent.neutral | hello        |
| smalltalk.agent.neutral | cool         |

The `smalltalk.agent.neutral` intent may be triggered by any of these phrases, or a variation based on DialogFlow's ML.

The intent column **MUST** match the intents in the intent csv file.

### How to upload agent?

In the DialogFlow console, goto `Settings > Export and Import > Import from Zip`

**IMPORTANT:** Intents and entities that you upload will replace existing intents and entities with the same name.