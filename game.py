import random
import requests

class WordGuesser:
    def __init__(self):
        try:
            response = requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words.txt')
            response.raise_for_status()
            words = [line.strip().lower() for line in response.text.splitlines() if line.strip()]
            # Filter to words 6 letters or under
            words = [word for word in words if len(word) <= 6]
        except requests.RequestException:
            raise ValueError("Unable to fetch words from the internet")
        if not words:
            raise ValueError("No words available")
        self.word = random.choice(words)
        self.guessed_letters = set()
        self.guessed_words = set()
        self.max_attempts = len(self.word) + 3
        self.attempts = 0
        self.display = ['_'] * len(self.word)

    def guess(self, entry):
        entry = entry.lower()
        if len(entry) == 1:
            if entry in self.guessed_letters:
                return "Already guessed!"
            self.guessed_letters.add(entry)
            if entry in self.word:
                for i, char in enumerate(self.word):
                    if char == entry:
                        self.display[i] = entry
                return f"Good guess! {''.join(self.display)}"
            else:
                self.attempts += 1
                remaining = self.max_attempts - self.attempts
                return f"Wrong guess! Attempts left: {remaining}. {''.join(self.display)}"
        else:
            if entry in self.guessed_words:
                return "Already guessed!"
            self.guessed_words.add(entry)
            if entry == self.word:
                self.display = list(self.word)
                return f"Good guess! {''.join(self.display)}"
            else:
                self.attempts += 1
                remaining = self.max_attempts - self.attempts
                return f"Wrong guess! Attempts left: {remaining}. {''.join(self.display)}"

    def is_won(self):
        return '_' not in self.display

    def is_lost(self):
        return self.attempts >= self.max_attempts

def main():
    game = WordGuesser()
    print(f"Guess the word! It has {len(game.word)} letters.")
    print(' '.join(game.display))

    while not game.is_won() and not game.is_lost():
        guess = input("Enter a letter or the entire word: ").strip()
        if not guess.isalpha():
            print("Please enter only letters.")
            continue
        print(game.guess(guess))

    if game.is_won():
        print(f"You won! The word was '{game.word}'.")
    else:
        print(f"You lost! The word was '{game.word}'.")

if __name__ == "__main__":
    main()