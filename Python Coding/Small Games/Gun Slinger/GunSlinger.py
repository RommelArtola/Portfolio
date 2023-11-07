"""Old School (Python) Standoff...

    Do you think you can draw faster than your opponent? Let's test it...
    1) Run the code
    2) Confirm to play
    3) When you see "DRAW" come up, press Enter. 
    4) To win, you have 0.3 seconds to draw.
    5) Confirm to play again by pressing enter or typing QUIT to stop.
"""
import random
import sys
import time

print('Classic Standoff\n')

print('Let\'s put your reflex to the test and see if you are the fastest in \n'
      'all of the land, or simply a phony!')

print()
print('When you see "DRAW", you have 0.3 seconds to press Enter.')
print('You lose if you draw BEFORE the prompt appears \n'
      'and if you don\'t draw quickly enough')
input('Press Enter to begin...')

while True:

    print('Round starting. Ready your aim...')
    print()

    time.sleep(random.randint(20, 50) / 10.0)
    print('DRAW! \U0001F52B')
    drawTime = time.time()
    input() # This function call doesn't return until Enter is pressed.
    timeElapsed = time.time() - drawTime
    if timeElapsed < 0.01:
        # If the player pressed Enter before DRAW! appeared, the input()
        # call returns almost instantly.
        print('You drew before "DRAW" appeared! You lose.')
    elif timeElapsed > 0.3:
        timeElapsed = round(timeElapsed, 4)
        print('You took', timeElapsed, 'seconds to draw. You lost.')
    else:
        timeElapsed = round(timeElapsed, 4)
        print('You took', timeElapsed, 'seconds to draw.')
        print('You are the fastest draw in the west! You win!')

    print('Enter QUIT to stop, or press Enter to play again.')
    response = input(':').upper()
    if response == 'QUIT':
        print('Thanks for playing!')
        sys.exit()