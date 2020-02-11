import pandas as pd
import argparse
import os
from pathlib import Path
from uuid import uuid4
import json
import shutil


parser = argparse.ArgumentParser(
    description='Generate DialogFlow Agents from CSV files!')
parser.add_argument('--name', nargs='?', default='agent',
                    help='Name of agent (Default: agent)')
parser.add_argument('--intents', nargs='?',
                    help='Select csv file to generate intent responses from.')
parser.add_argument('--phrases', nargs='?',
                    help='Select csv file to generate training phrases from.')
parser.add_argument('-o', '--output', nargs='?', default='agent',
                    help='Name of output zip. (without .zip at the end)')
parser.add_argument('-z', '--zip', action='store_true',
                    help='Create zip file automatically.')
parser.add_argument('-V', '--version', type=str, default='1.0.0',
                    help='Set a version (Default: 1.0.0)')
args = parser.parse_args()

if args.intents is None and args.phrases is None:
    print('Provide an intents or phrases file. Or try -h for help.')
    exit()

if args.zip:
    root_fp = os.path.abspath('temp_agent')
else:
    root_fp = os.path.abspath(args.name)

intent_fp = root_fp+os.path.sep+'intents'
Path(intent_fp).mkdir(parents=True, exist_ok=True)


def new_phrase(phrase):
    _id = str(uuid4())
    phrase_obj = {
        "id": _id,
        "data": [
            {
                "text": phrase[0],
                "userDefined": False
            }
        ],
        "isTemplate": False,
        "count": 0,
        "updated": 0
    },

    return phrase_obj


def new_message(variants):
    message = {
        "type": 0,
        "lang": "en",
        "speech": variants
    }
    return message


def new_intent(name, responses):
    _id = str(uuid4())
    messages = []
    for res in responses:
        messages.append([x for x in res if str(x) != 'nan'])

    messages = [new_message(x) for x in messages]

    intent_object = {
        "id": _id,
        "name": name,
        "auto": True,
        "contexts": [],
        "responses": [
            {
                "resetContexts": False,
                "affectedContexts": [],
                "parameters": [],
                "messages": messages,
                "defaultResponsePlatforms": {
                    "google": True
                },
                "speech": []
            }
        ],
        "priority": 500000,
        "webhookUsed": False,
        "webhookForSlotFilling": False,
        "fallbackIntent": False,
        "events": [],
        "conditionalResponses": [],
        "condition": "",
        "conditionalFollowupEvents": []
    }

    return intent_object


def generate_package_json():
    # Must have package.json in agent.zip
    with open(root_fp+os.path.sep+'package.json', "w+") as f:
        content = {
            "version": args.version
        }
        json.dump(content, f, indent=2)


def generate_file(filetype, columns, source_filepath):
    df = pd.read_csv(source_filepath, index_col=False)
    if not set(columns).issubset(df.columns):
        print('Invalid column names. \nRequire first row to be column titles:')
        [print('"'+c+'"') for c in columns]
        return

    df.sort_values(columns[0], inplace=True)
    df.drop_duplicates(keep='first', inplace=True)
    # df = df[columns]  # Only take what you need
    df['combined'] = df.drop('intent', axis=1).values.tolist()
    columns.append('combined')
    df = df[columns]

    grouped_df = df.groupby(columns[0])

    for row in grouped_df.agg(list).iterrows():
        first_col = row[0]
        second_col = row[1].combined

        json_data = None
        if filetype == 'intents':
            fp = intent_fp + os.path.sep + first_col + '.json'
            json_data = new_intent(first_col, second_col)
        elif filetype == 'phrases':
            fp = intent_fp + os.path.sep + first_col + '_usersays_en.json'
            json_data = [new_phrase(phrase)[0]
                         for phrase in second_col]
        else:
            return

        f = open(fp, 'w+')
        json.dump(json_data, f, indent=2, sort_keys=False)
        f.close()
    print('Generated '+filetype+' files.')


if args.intents and os.path.isfile(args.intents):
    generate_file('intents', ['intent'], args.intents)

if args.phrases and os.path.isfile(args.phrases):
    generate_file('phrases', ['intent', 'phrase'], args.phrases)

if args.intents or args.phrases:
    generate_package_json()
    print('package.json created with version: '+args.version)
    print('Agent files generated!')

# Create zip file of agent.
if args.zip:
    if args.output:
        zipname = args.output
    else:
        zipname = args.name+'-'+args.version
    shutil.make_archive(zipname, 'zip', root_fp)
    shutil.rmtree(root_fp)
    print('Zip file "'+zipname+'.zip" created!')
else:
    print('Compress the folder into a zip to import to dialogflow.')
    print('Or run this script with "-z" option to generate zipfile automatically.')
