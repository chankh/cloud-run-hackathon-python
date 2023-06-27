
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['L', 'R']
last_action = ''

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    
    # TODO add your implementation here to replace the random response
    input = request.json
    my_state = {}
    mylink = input["_links"]["self"]["href"]
    arena = input['arena']
    width = arena['dims'][0]
    height = arena['dims'][1]
    arena_map = [[None for x in range(width)] for y in range(height)]
    state = arena['state']
    for k in state:
        v = state[k]
        x = v['x']
        y = v['y']
        print("{}, {} is {}".format(y, x, k))
        arena_map[y][x] = k
        if k == mylink:
            my_state = v

    global last_action
    action = last_action
    if action != 'R' or action != 'L':
        action = moves[random.randrange(len(moves))]

    if someone_in_front(my_state, arena_map, width, height):
        action = 'T'
    elif not facing_wall(my_state, width, height):
        action = 'F'

    
    print("action: " + action)
    last_action = action
    return action

def facing_wall(my_state, width, height):
    d = my_state['direction']
    x = my_state['x']
    y = my_state['y']

    if d == 'N' and y == 0:
        return True
    if d == 'W' and x == 0:
        return True
    if d == 'S' and y == height - 1:
        return True
    if d == 'E' and x == width -1:
        return True

    return False


def someone_in_front(my_state, arena, width, height):
    d = my_state['direction']
    x = my_state['x']
    y = my_state['y']

    print("direction: {}, x: {}, y: {}".format(d, x, y))
    if d == 'N':
        if y-1 >= 0 and arena[y-1][x] is not None:
            print("Target {} at {}, {}".format(arena[y-1][x], y-1, x))
            return True
        if y-2 >= 0 and arena[y-2][x] is not None:
            print("Target {} at {}, {}".format(arena[y-2][x], y-2, x))
            return True
        if y-3 >= 0 and arena[y-3][x] is not None:
            print("Target {} at {}, {}".format(arena[y-3][x], y-3, x))
            return True
    elif d == 'W':
        if x-1 >= 0 and arena[y][x-1] is not None:
            print("Target {} at {}, {}".format(arena[y][x-1], y, x-1))
            return True
        if x-2 >= 0 and arena[y][x-2] is not None:
            print("Target {} at {}, {}".format(arena[y][x-2], y, x-2))
            return True
        if x-3 >= 0 and arena[y][x-3] is not None:
            print("Target {} at {}, {}".format(arena[y][x-3], y, x-3))
            return True
    elif d == 'E':
        if x+1 < width and arena[y][x+1] is not None:
            print("Target {} at {}, {}".format(arena[y][x+1], y, x+1))
            return True
        if x+2 < width and arena[y][x+2] is not None:
            print("Target {} at {}, {}".format(arena[y][x+2], y, x+2))
            return True
        if x+3 < width and arena[y][x+3] is not None:
            print("Target {} at {}, {}".format(arena[y][x+3], y, x+3))
            return True
    elif d == 'S':
        if y+1 < height and arena[y+1][x] is not None:
            print("Target {} at {}, {}".format(arena[y+1][x], y+1, x))
            return True
        if y+2 < height and arena[y+2][x] is not None:
            print("Target {} at {}, {}".format(arena[y+2][x], y+2, x))
            return True
        if y+3 < height and arena[y+3][x] is not None:
            print("Target {} at {}, {}".format(arena[y+3][x], y+3, x))
            return True
    else:
        return False

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
