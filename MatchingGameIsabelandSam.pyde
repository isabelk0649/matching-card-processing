import random
import os
import json
import pickle

# application configuration
configoption = random.randint(1,2)
#configoption = 2
# name of the json config file
config = 'config' + str(configoption) + '.json'


# required accommodate different windows sizes
def settings():
    if configoption == 1:
        #4x5 cards each card occupies 100x150 area
        size(510, 610)
    elif configoption == 2:
        #4x4 cupcakes each cupcake occupies 100x100 area
        size(410, 410)
    else:
        #defaults to 4x5 cards
        size(510, 610)
        
add_library("minim")
    
def setup():
    
    global configoption
    global deck
    global bg_img, menu_img, gameover_img, help_img, scores_img
    
    global cards_to_play
    global num_cards_to_play, num_cards_to_match
    # list of boolean
    global cards_to_play_matched
    global cards_to_draw
    
    global cards_counter 
    global cards_matched
    
    global user_clicks
    global user_selections
    
    
    global card_rect, card_height, card_width, cards_per_row, cards_per_column
    global x0, y0
    
    global keyp
    global playername
    global mode
    global starttime
    global time_exceeded
    global scores
    global score
    global window_size
    global start_button, replay_button, help_button, scores_button, back_button, menu_button
    global fontsize
    global scores_rect
    global music
    
    minim = Minim(this)
    music = minim.loadFile("sweden.mp3")

    background(0)
    
    time_exceeded = False
    
    keyp =""    
    playername = ""
    
    #modelist = ["start", "play", "scores", "help", "gameover", "getname"]
    
    # set mode 'start'
    mode = 'start'
    starttime = millis()
    scores = {}
    score = 0

    # read scores from disk if present
    if os.path.isfile('scores.pkl'):
        with open('scores.pkl', 'rb') as fh:
            scores = pickle.load(fh)
    else:
        # if not initialize scores dict
        scores = {}
        
    # read configuration from json file.
    # name of the json file depend on the option (1,2)
    setup_info = json.load(open(config))
    num_cards_to_play = setup_info['num_cards_to_play']
    num_cards_to_match = int(num_cards_to_play/2)
    cards_per_row = setup_info['cards_per_row']
    cards_per_column = setup_info['cards_per_column']

    #card_rect = (100, 150)
    card_rect = setup_info['card_rect']
    card_width=setup_info['card_width']
    card_height=setup_info['card_height']
        
    x0 = setup_info['x0']
    y0 = setup_info['y0']
    
    #size_x = cards_per_row*100+x0 # 5*100+10
    #size_y = cards_per_column*150+y0 # 4*150+10
    window_size = setup_info['window_size']
    start_button = setup_info['start_button']
    replay_button = setup_info['replay_button']
    help_button = setup_info['help_button']
    scores_button = setup_info['scores_button']
    back_button = setup_info['back_button']
    menu_button = setup_info['menu_button']
    
    fontsize = setup_info['fontsize']
    scores_rect = setup_info['scores_rect']
    
    user_clicks = 0

    cdir=os.path.curdir
    print("Current directory: ", os.path.abspath(cdir))


    # common images for both options
    menu_img = loadImage( "menu.png" )
    gameover_img = loadImage( "gameover.png" )
    help_img = loadImage( "help.png" )
    scores_img = loadImage( "scores.png" )
    
        
    deck = []
    cards_to_play = []
    cards_to_play_matched = []
    cards_to_draw = []
    cards_counter = {}
    cards_matched = []
    user_selections = []

    print("Config: ", config)
    # images
    if configoption == 1:
        bg_img = loadImage( "back_of_card.png" )
        cardspath = os.path.join(cdir,'data','cards')
    else:
        bg_img = loadImage( "back_of_cupcake.jpg" )
        cardspath = os.path.join(cdir,'data','cupcakes')

    for file in os.listdir(cardspath):
        if os.path.isfile(os.path.join(cardspath, file)):
            deck.append(loadImage(os.path.join(cardspath, file)))

    print('Deck size: ', len(deck))
    #for i,c in enumerate(deck):
    #    print(i, 'Image: ', c)
        
    print("Window size: ", window_size)
    p = [x for x in range(1,len(deck)+1)]
    rnd_cards = random.sample(p,num_cards_to_play/2)
    rnd_cards.extend(random.sample(rnd_cards,num_cards_to_play/2))
    
    print("Random sample: ", rnd_cards)
    # This is for testing only. Comment subsequent line when running the program 
    # click the following: (0,14), (1,16), (2,12), (3,11), (4,18), (5,10), (6,14), (7,17), (8,15), (9,19)
    #rnd_cards = [39, 13, 19, 26, 51, 41, 25, 16, 27, 7, 41, 26, 19, 39, 25, 27, 13, 16, 51, 7]
     
    for c in rnd_cards:
        cards_to_play.append(deck[c-1])
        cards_to_draw.append(bg_img)
        cards_to_play_matched.append(False)
            
    #print("Cards to play: ", cards_to_play)
    #print("Cards to draw: ", cards_to_draw)
    
    noLoop()
    
def reshuffle_cards():
    
    global num_cards_to_play
    global deck
    global cards_to_play
    global cards_to_play_matched
    global cards_to_draw
    
    cards_to_play = []
    cards_to_play_matched = []
    cards_to_draw = []
    cards_matched = []
    user_selections = []
    
    user_clicks = 0
    cards_counter = {}
    score = 0
    
    p = [x for x in range(1,len(deck)+1)]
    rnd_cards = random.sample(p,num_cards_to_play/2)
    rnd_cards.extend(random.sample(rnd_cards,num_cards_to_play/2))
    
    print('Reshuffling')
    for c in rnd_cards:
        cards_to_play.append(deck[c-1])
        cards_to_draw.append(bg_img)
        cards_to_play_matched.append(False)
    
def reset_vars():
    
    global num_cards_to_play
    global deck
    
    global cards_to_play
    global cards_to_play_matched
    global cards_to_draw
    global cards_matched
    global user_selections
    
    global user_clicks
    global cards_counter
    global score
    
    global starttime
    global time_exceeded
    
    if mode == 'start':
        print('Reset variables')
    
        cards_to_play = []
        cards_to_play_matched = []
        cards_to_draw = []
        cards_matched = []
        user_selections = []
    
        user_clicks = 0
        cards_counter = {}
        score = 0
    
        p = [x for x in range(1,len(deck)+1)]
        rnd_cards = random.sample(p,num_cards_to_play/2)
        rnd_cards.extend(random.sample(rnd_cards,num_cards_to_play/2))
    
        starttime = millis()
        time_exceeded = False
        
        print('Generate new cards to play')
        for c in rnd_cards:
            cards_to_play.append(deck[c-1])
            cards_to_draw.append(bg_img)
            cards_to_play_matched.append(False)

def draw():
    global mode, window_size
    global fontsize, scores_rect
    global time_exceeded
    global music
    
    music.play()
    background(0)
    
    if mode == 'start':
        # if mode is 'start' -> display main menu
        image(menu_img, 0, 0, window_size[0], window_size[1])
        
    elif mode == 'getname':
        # if mode is 'getname' -> display text
        textSize(fontsize)
        fill(255)
        if configoption == 1:
            text('ENTER YOUR NAME (Press Enter to Play): ', 10, 550)
            text(playername, 210, 580)
        else:
            text('ENTER YOUR NAME (Press Enter to Play): ', 10, 350)
            text(playername, 160, 380)
        
    elif mode == 'play':
        # if mode play and we haven't matched all cars
        if not check_if_all_cards_matched():
            for i,img in enumerate(cards_to_draw):
                y,x = divmod(i, cards_per_row)
                a = x0 + x*card_rect[0]
                b = y0 + y*card_rect[1]
                # check if card was matched then remove it by filling the space with back
                if cards_to_play_matched[i]:
                    fill(0)
                    rect(a, b, card_width, card_height);
                else:
                    image(img, a, b, card_width, card_height)
                
            
    elif mode == 'gameover':
        if time_exceeded:
            # if mode is gameover then we exceeded the time. we display game over menu including scores
            image(gameover_img, 0, 0, window_size[0], window_size[1])
            upper_left_yellow_box = [70,140]
            fill(0) 
            textSize(fontsize)
            offset_x = 10
            offset_y = 10
            text('TIME LIMIT EXCEEDED', upper_left_yellow_box[0] + offset_x, upper_left_yellow_box[1] + offset_y)
            text(playername + " : " + str(score), upper_left_yellow_box[0] + offset_x, upper_left_yellow_box[1] + offset_y + 30)
        else:
            image(gameover_img, 0, 0, window_size[0], window_size[1])
            upper_left_yellow_box = [70,140]
            fill(0) 
            textSize(fontsize)
            offset_x = 10
            offset_y = 10
            text('YOU WON!', upper_left_yellow_box[0] + offset_x, upper_left_yellow_box[1] + offset_y)
            text(playername + " : " + str(score), upper_left_yellow_box[0] + offset_x, upper_left_yellow_box[1] + offset_y + 30)
        
    elif mode == 'scores':
        # is mode is scores the display scores for all players.
        # for each player we display the highest score
        image(scores_img, 0, 0, window_size[0], window_size[1])
        upper_left_yellow_box = [70,140]
        fill(0) 
        textSize(fontsize)
        offset_x = 10
        offset_y = 10
        for k,v in scores.items():
            text(k + " : " + str(max(v)), upper_left_yellow_box[0] + offset_x, upper_left_yellow_box[1] + offset_y)
            offset_y += 30
        
        #scores serialize to disk

    elif mode == 'help':
        # if mode is help the show the help screen
        image(help_img, 0, 0, window_size[0], window_size[1])
        
def check_if_all_cards_matched():
    global num_cards_to_match
    #print('num_cards_to_match: ', num_cards_to_match)
    #print('cards_to_play_matched: ', len(cards_matched))
    if len(cards_matched) < num_cards_to_match:
        return False
    return True
 

def matching_last_2_cards():
    global user_selections
    global score
    
    print("BEGIN MATCHING-2")
    last_idx, last_img = user_selections[len(user_selections) - 1]
    second_last_idx, second_last_img = user_selections[len(user_selections) - 2]
    print("Cards [idx]: ", second_last_idx, last_idx)
    # possible matching
    if last_img == second_last_img:
        if last_idx == second_last_idx:
            # Not a match. We clicked on the same card twice. Flip back to bg 
            print("NOT A MATCH. The same card (", last_idx, ") was selected twice.")
            if cards_to_play_matched[last_idx] == False:
                cards_to_draw[last_idx] = bg_img
                    
            # remove second last and last selections from the user_selections 
            user_selections.pop(len(user_selections)-2)
            user_selections.pop(len(user_selections)-1)
        else:
            if (second_last_idx, last_idx) not in cards_matched:
                print("Cards [idx]:", second_last_idx, last_idx, " MATCH")
                cards_matched.append((second_last_idx, last_idx))
                cards_to_play_matched[second_last_idx] = True
                cards_to_play_matched[last_idx] = True
                # increment score
                score+=1

                    
            # remove second last and last selections from the user_selections
            print("Removing cards: ", second_last_idx, last_idx, " from user_selections.")
            user_selections.pop(len(user_selections)-2)
            user_selections.pop(len(user_selections)-1)
    else:
        print("Cards [idx]:", second_last_idx, last_idx, " DO NOT MATCH")
            
    print("END MATCHING-2")
    
    
def matching_last_3_cards():
    # matching happens when we have selected 3 cards
    print("BEGIN MATCHING-3")
    third_last_idx, third_last_img = user_selections[len(user_selections) - 3]
    second_last_idx, second_last_img = user_selections[len(user_selections) - 2]
    last_idx, last_img = user_selections[len(user_selections) - 1]
    # check if we have a match between the cards (card must have the same img but different idx must match)
    print("Cards [idx]: ", third_last_idx, second_last_idx, last_idx)
    if third_last_img != second_last_img:
        print("Cards [idx]:", third_last_idx, second_last_idx, " DO NOT MATCH")
        if cards_to_play_matched[third_last_idx] == False:
                cards_to_draw[third_last_idx] = bg_img
        if cards_to_play_matched[second_last_idx] == False:
                cards_to_draw[second_last_idx] = bg_img
                    
        print("Removing cards: ", third_last_idx, second_last_idx, " from user_selections.")       
        user_selections.pop(len(user_selections)-3)
        user_selections.pop(len(user_selections)-2)

    print("END MATCHING-3")

def button_clicked(button_area):
    if button_area[0][0] <= mouseX <= button_area[1][0]:
        if button_area[0][1] <= mouseY <= button_area[1][1]:
            return True
    return False

def clicked_on_start_button():
    global start_button
    if start_button[0][0] <= mouseX <= start_button[1][0]:
        if start_button[0][1] <= mouseY <= start_button[1][1]:
            return True
    return False
     
def clicked_on_replay_button():
    #if 30 <= mouseX <= 160:
    #    if 550 <= mouseY <= 610:
    #        print('Clicked on Replay button')
    #        return True
    global replay_button
    if replay_button[0][0] <= mouseX <= replay_button[1][0]:
        if replay_button[0][1] <= mouseY <= replay_button[1][1]:
            return True
    return False
    
def clicked_on_help_button():
    #if 190 <= mouseX <= 320:
    #    if 550 <= mouseY <= 610:
    #        print('Clicked on Help button')
    #        return True
    global help_button
    if help_button[0][0] <= mouseX <= help_button[1][0]:
        if help_button[0][1] <= mouseY <= help_button[1][1]:
            return True
    return False

def clicked_on_scores_button():
    #if 350 <= mouseX <= 480:
    #    if 550 <= mouseY <= 610:
    #        print('Clicked on Scores button')
    #        return True
    global scores_button
    if scores_button[0][0] <= mouseX <= scores_button[1][0]:
        if scores_button[0][1] <= mouseY <= scores_button[1][1]:
            return True
    return False

def clicked_on_back_button():
    #if 185 <= mouseX <= 325:
    #    if 550 <= mouseY <= 610:
    #        print('Clicked on Back button')
    #        return True
    global back_button
    if back_button[0][0] <= mouseX <= back_button[1][0]:
        if back_button[0][1] <= mouseY <= back_button[1][1]:
            return True
    return False
    
def clicked_on_menu_button():
    #if 185 <= mouseX <= 325:
    #    if 550 <= mouseY <= 610:
    #        print('Clicked on Menu button')
    #        return True
    global menu_button
    if menu_button[0][0] <= mouseX <= menu_button[1][0]:
        if menu_button[0][1] <= mouseY <= menu_button[1][1]:
            return True
    return False

def update_scores():
    global mode
    global cards_matched
    global scores

    if scores.has_key(playername):
        # add the score to the list of scores
        #scores[playername].append(len(cards_matched))
        scores[playername].append(score)
    else:
        # set the fist score in the list
        scores[playername] = [score]


def mouseClicked():
    
    global user_clicks
    global cards_selected
    global user_selections
    global cards_to_play_matched
    global mode
    global score
    global playername
    global starttime 
    global time_exceeded
    
    # ["start", "play", "getname", "scores", "help", "gameover"]
    print('-----------------------------------------')
    print('BEGIN mouse clicked at: ', (mouseX, mouseY))
    print('BEGIN game mode: ', mode)
    print("BEGIN player name: ", playername)
    print('BEGIN player score: ', score)
    print('BEGIN scores: ', scores)

    if mode == 'start':
        # if mode is 'start' user can click on multiple buttons
        if clicked_on_start_button():
            print('START BUTTON clicked')
            # reset variables
            reset_vars()
            # reset player name
            playername = ""
            # change mode to from 'start -> 'getname'
            mode = 'getname'
        elif clicked_on_replay_button():
            # change mode to from 'start -> 'play'
            print('REPLAY BUTTON clicked')
            if not playername == "":
                reset_vars()
                # keep the same player name
                mode = 'play'
            else:
                pass
                
        elif clicked_on_scores_button() == True:
            print('SCORES BUTTON clicked')
            # shoud we serialize here? I guess so.
            with open('scores.pkl', 'wb') as fh:
                pickle.dump(scores, fh)
            # change mode to from 'start -> 'scores'
            mode = 'scores'
                
        elif clicked_on_help_button() == True:
            # change mode to 'help'
            print('HELP BUTTON clicked')
            #print('changing mode to help')
            mode = 'help'
                
    elif mode == 'play':
        # if mode is 'play'
        # check if time exceeded
        if millis() - starttime > 60000:
            # if elapsed is more than 60s then game over due to timeout
            print('GAME OVER.TIME EXCEEDED')
            time_exceeded = True
            # set mode to 'gameover'
            mode = 'gameover'
            update_scores()
        elif check_if_all_cards_matched():
            print("**************************")
            print("*** GAME OVER.YOU WON. ***")
            print("**************************")
            # all cards have been matched
            mode = 'gameover'
            update_scores()
        else:
            # game is still on (mode is 'play' and there are cards to match)
            # continue game
            print('GAME CONTINUES')
            process_user_action()
            # check if we've matched all cards
            if check_if_all_cards_matched():
                print('GAME OVER. YOU WON.')
                mode = 'gameover'
                update_scores()
        
    elif mode == 'scores':
        # mode is scores 
        if clicked_on_back_button():
            print('HELP BUTTON clicked')
            # change mode from 'scores' -> 'start'
            mode='start'
        
    elif mode == 'gameover':
        # if mode is gameover (user has won the game) 
        # user can click only on menu button which will restart the game
        if clicked_on_menu_button():
            print('MENU BUTTON clicked')
            # change mode from 'gameover' to 'start'
            mode = 'start'
            # reset variables
            reset_vars()
            
    elif mode == 'help':
        # mode is help
        if clicked_on_back_button():
            # change mode from 'help' to 'start'
            print('BACK BUTTON clicked')
            mode = 'start'

    print('END player score: ', score)
    print('END scores: ', scores)            
    print('END game mode: ', mode)
    print('-----------------------------------------')
    
    loop()  
        
def process_user_action():
    
    global user_clicks
    global user_selection
    
    is_card_locked = False
    
    print("*******************************************")
    print('BEGIN process_user_action')
    print("BEGIN Clicked:", user_clicks, len(user_selections), user_selections)
    print("BEGIN Cards to play with matches: ", cards_to_play_matched)
    print("BEGIN Cards matched: ", cards_matched)
    print("Player Name: ", playername)
    
    print("Time exceeded: ", time_exceeded)
    elapsed = round((millis() - starttime)/1000)
    print("Elapsed time: ", elapsed)
    print("Remaining time: ", 60 - elapsed)
    
    # increment number of clicks
    user_clicks = user_clicks+1
    
    # determine the position of the cards based on the user selection (area of the screen in whihc the user has clicked)
    x_quot,x_rem = divmod(mouseX, card_rect[0])
    y_quot,y_rem = divmod(mouseY, card_rect[1])
    
    # selection_idx = integer valuable which takes values from 0 to len(cards_to_play)
    # and represents the position of the card from the list (cards_to_play)
    selection_idx = y_quot*cards_per_row + x_quot
    print("Selection Idx: ", selection_idx)
    # fetch the card (face up) that correspond to the selected position
    if selection_idx >= len(cards_to_play):
        # this happens when user clicks outside the border
        print("User selection is oustside of the card area.") 
        selection_idx = len(cards_to_play) - 1
    
    selection_img = cards_to_play[selection_idx]
    print("Position selected: ", selection_idx)
    # increment counters
    if selection_idx in cards_counter:
        cards_counter[selection_idx]+=1
    else:
        # first time encountered
        cards_counter[selection_idx] = 1
        
    # add selected cards to user_selections (if not matched already) 
    if cards_to_play_matched[selection_idx]:
        # if selected card has been matched already do not append to user_selections
        is_card_locked = True
    else:
        # append selected card to user_selections
        user_selections.append((selection_idx, selection_img))

    last_idx = selection_idx
    last_img = selection_img
    second_last_idx = None
    second_last_img = None
    third_last_idx = None
    third_last_img  = None
    
    # if last card selected hasn't been matched (not locked) flip the card face up 
    if not is_card_locked:
        if cards_to_draw[last_idx] == bg_img:
            cards_to_draw[last_idx] = cards_to_play[last_idx]
            print("Card at position ", selection_idx, " face up: ", cards_to_draw[last_idx])
        else:
            cards_to_draw[last_idx] = bg_img
            print("Card at position ", selection_idx, " face down: ", cards_to_draw[last_idx])
    else:
        print("Card at position ", selection_idx, " is already matched.")
    
    if len(user_selections) == 1:
        print("BEGIN MATCHING-1")
        print("Cards [idx]: ", last_idx)
        print("END MATCHING-1")
        
    elif len(user_selections) == 2:
        matching_last_2_cards()
    elif len(user_selections) == 3:
        matching_last_3_cards()
    else:
        # END 
        print("BEGIN DEFAULT")
        print("WARNING: SOMETHING WENT WRONG!")
        print("END DEFAULT")
        
    print("All cards matched?: ", check_if_all_cards_matched())
    print("Cards hit counters: ", cards_counter)
    print("Total cards matched: ", len(cards_matched))
    print("END Cards [idx] matched: ", cards_matched)
    print("END Cards to play (matched): ", cards_to_play_matched)
    print("END Clicked: ", user_clicks, len(user_selections), user_selections)
    print('END process_user_action')
    print("*******************************************")
    
    
    
def keyReleased():
    global keyp, mode, playername
    keyp = key
    print('keyReleased. Key: ',key) 
    if mode == 'getname':
        if keyp != ENTER:
            playername+= keyp.upper()
        else:
            #print('keyReleased: ', 'ENTER')
            print('keyReleased. Player name: ', playername)
            # change mode to from 'getname -> 'play'
            mode = 'play'

    loop()    
