#!/usr/bin/python

from game import Game
import console as c

game = None

def welcome():
    c.clear_screen()
    c.welcome()

def create_game():
    global game
    num_players = c.request_num_players()
    num_cards_each = c.request_num_cards_each()
    player_names = []
    for i in range(num_players):
        player_name = c.request_player_name(i)
        player_names.append(player_name)
    game = Game(num_players, num_cards_each, player_names)
    game.deal()
    c.clear_screen()
    c.show_game(game)
    c.wait_user()

def swap_cards():
    global game
    for player in game.players:
        c.clear_screen()
        c.show_player_swap(player)
        swap = c.request_swap(player.name)
        while swap:
            c.clear_screen()
            c.show_player_swap(player)
            hCard = c.request_hand_swap() - 1
            fCard = c.request_faceup_swap() - 1
            player.swap(hCard, fCard)
            c.clear_screen()
            c.show_player_swap(player)
            swap = c.request_swap_more()

def first_move():
    global game
    game.first_move()
    c.clear_screen()
    c.show_game(game)
    c.line()

def main_game():
    global game
    while game.continue_game():
        if game.playing_from_face_down():
            make_facedown_move()
        else:
            if game.can_play():
                make_move()
            else:
                c.show_pickup(game.current_player())
                c.wait_user()
                game.pickup()
                continue_main_game()

def continue_main_game():
    global game
    c.clear_screen()
    c.show_game(game)
    c.line()
    main_game()

def make_move():
    global game
    card_indexes = c.request_move(game.current_player())
    cards = game.get_cards(card_indexes)
    if not game.valid_move(cards):
        c.bad_move(cards)
        make_move()
    else:
        game.lay_cards(cards)
        continue_main_game()

def make_facedown_move():
    global game
    card_index = c.request_from_face_down(game.current_player())
    cards = game.get_cards([card_index])
    if not game.valid_move(cards):
        c.show_bad_facedown_choice(cards)
        c.wait_user()
        game.pickup_with_facedown_card(cards)
    else:
        game.lay_cards(cards)
    continue_main_game()
        
def end_game():
    global game
    pythonhead = game.get_pythonhead()
    c.show_pythonhead(pythonhead)
    c.wait_user()

def main():
    welcome()
    create_game()
    swap_cards()
    first_move()
    main_game()
    end_game()

if __name__ == "__main__":
    main()
