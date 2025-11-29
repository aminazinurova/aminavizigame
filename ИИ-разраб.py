import tkinter as tk
from tkinter import ttk, messagebox
import random
class MemoryGameApp:
    def _ai_make_move(self):
        if self.game_over or self.current_player != "Computer":
            return
        self.can_click = False 
        card1_idx = -1
        card2_idx = -1
        for symbol, indices in self.ai_memory.items():
            unmatched_indices = [idx for idx in indices if not self.cards[idx]["is_matched"] and not self.cards[idx]["is_revealed"]]
            if len(unmatched_indices) >= 2:
                card1_idx = unmatched_indices[0]
                break
        if card1_idx == -1:
            unrevealed_unmatched_cards = [
                i for i, card in enumerate(self.cards)
                if not card["is_revealed"] and not card["is_matched"]
            ]
            if not unrevealed_unmatched_cards: 
                self._game_over()
                return
            card1_idx = random.choice(unrevealed_unmatched_cards)

        self._simulate_card_click(card1_idx, is_ai=True)
        self.master.after(1000, lambda: self._ai_second_move_decision(card1_idx, card2_idx))

    def _ai_second_move_decision(self, first_card_idx, known_second_card_idx):

        if self.game_over or self.current_player != "Computer":
            return
        second_card_idx = -1
        first_card_symbol = self.cards[first_card_idx]["symbol"]

        if known_second_card_idx != -1 and not self.cards[known_second_card_idx]["is_revealed"] and not self.cards[known_second_card_idx]["is_matched"]:
            second_card_idx = known_second_card_idx

        elif first_card_symbol in self.ai_memory:
            potential_matches = [
                idx for idx in self.ai_memory[first_card_symbol]
                if idx != first_card_idx and not self.cards[idx]["is_matched"] and not self.cards[idx]["is_revealed"]
            ]
            if potential_matches:
                second_card_idx = random.choice(potential_matches) 
                        
        if second_card_idx == -1:
            second_card_idx = self._ai_pick_random_unrevealed(first_card_idx)

        self._simulate_card_click(second_card_idx, is_ai=True)


    def _ai_pick_random_unrevealed(self, exclude_idx):
        unrevealed_unmatched_cards = [
            i for i, card in enumerate(self.cards)
            if not card["is_revealed"] and not card["is_matched"] and i != exclude_idx
        ]
        if not unrevealed_unmatched_cards:
            return -1 
        return random.choice(unrevealed_unmatched_cards)

    def _simulate_card_click(self, card_idx, is_ai=False):
        if self.game_over or (is_ai and self.current_player != "Computer"):
            return

        card_info = self.cards[card_idx]

        if card_info["is_revealed"] or card_info["is_matched"]:
            return

        if len(self.flipped_cards) == 2:
            return

        self._flip_card(card_idx, reveal=True)
        self.flipped_cards.append(card_idx)

        symbol = card_info["symbol"]
        if symbol not in self.ai_memory:
            self.ai_memory[symbol] = []
        if card_idx not in self.ai_memory[symbol]:
            self.ai_memory[symbol].append(card_idx)

        if len(self.flipped_cards) == 2:
            self.can_click = False 

            self.moves += 1
            self.moves_label.config(text=f"Попытки: {self.moves}")
            
            card1_idx, card2_idx = self.flipped_cards
            card1_symbol = self.cards[card1_idx]["symbol"]
            card2_symbol = self.cards[card2_idx]["symbol"]

            if card1_symbol == card2_symbol:
                self.match_count += 1
                self.player_scores[self.current_player] += 1
                self.cards[card1_idx]["is_matched"] = True
                self.cards[card2_idx]["is_matched"] = True

                self.cards[card1_idx]["canvas"].itemconfig("border", fill=self.colors['card_matched_bg'])
                self.cards[card2_idx]["canvas"].itemconfig("border", fill=self.colors['card_matched_bg'])

                if card1_symbol in self.ai_memory:
                    self.ai_memory[card1_symbol] = [idx for idx in self.ai_memory[card1_symbol] if idx not in (card1_idx, card2_idx)]
                    if not self.ai_memory[card1_symbol]:
                        del self.ai_memory[card1_symbol]

                self._update_scores()
                self.flipped_cards = []
                self.master.after(700, self._check_game_over_or_continue_turn)
            else:
                self.master.after(1200, self._flip_back_and_switch_turn)

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryGameApp(root)
    root.mainloop()

