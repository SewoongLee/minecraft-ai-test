from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
import MalmoPython 
import os
import sys
import time
import json
import math

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
agent_host.parse( sys.argv )

# -- set up the mission -- #
mission_file = f'./{os.path.splitext(os.path.basename(__file__))[0]}.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    my_mission = MalmoPython.MissionSpec(f.read(), True)
agent_host.startMission(my_mission, MalmoPython.MissionRecordSpec() )

# Loop until mission starts:
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)
print()
print("Mission running")

def sendCommand(cmd):
    time.sleep(.5); agent_host.sendCommand(cmd); time.sleep(.5)

from llm import *
llm = LLM('chatgpt_35_turbo.exe')
# response = llm.send('Who are you? What version are you? Please introduce yourself.')

with open('prompt_tutorial.txt', 'r', encoding='utf-8') as file: content = file.read()
response = llm.send(content)

def askLLM(prompt_command):
    response = llm.send(prompt_command)

    print('Parsing response...')
    try:
        # Extract the substring between '[' and ']' and evaluate it as a list
        start_index = response.rfind('[')
        end_index = response.rfind(']')
        # Convert the string representation of the list to an actual list
        if start_index == -1 or end_index == -1: raise ValueError
        print(f'Parser: Found list of commands ({start_index}-{end_index})!')
        cmds = eval(response[start_index:end_index+1])
    except:
        # Fine occurrences of commands in the response

        import re
        response = response.replace(' use ', '').replace(' Use ', '')  # Remove 'use' when it is used as a verb
        splited = re.split(r'''[ .:\n\\'"]''', repr(response))
        # print('response: ', splited)

        COMMANDS = ['use', 'movenorth', 'moveeast', 'movesouth', 'movewest', 'attack']
        cmds = [cmd.strip().lower() for cmd in splited if cmd.strip().lower() in COMMANDS]
    
    print(f'Parsed: {cmds}')
    for cmd in cmds:
        sendCommand(cmd)

# askLLM('Build V.')
askLLM('What sequence of actions would place a V-shaped block?')
# askLLM('What sequence of actions would place a V-shaped block in the form of a staircase with two steps each on the left and right?')
askLLM('Destroy V.')

print()
print("Mission ended")
