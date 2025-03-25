import random
import time
from typing import List, Dict, Callable, Generator, Any, Optional, Union
import json
import os
import sys

class Question:
    def __init__(self, text: str, answer: str, options: List[str], difficulty: str):
        self.text = text
        self.answer = answer
        self.options = options
        self.difficulty = difficulty
        
        # Validate the answer is in options
        assert answer in options, f"Answer '{answer}' not found in options!"

class QuizGame:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.current_question = None
        self.total_questions = 0
        self.player_name = None
        self.high_scores = []
        
        # Try to load high scores from file
        try:
            with open("high_scores.json", "r") as f:
                self.high_scores = json.load(f)
        except:
            # If file doesn't exist or is corrupted, start with empty high scores
            self.high_scores = []
        
        # Global configuration for the game
        self.config = {
            "time_limit": 30,  # seconds per question
            "difficulty_levels": ["easy", "medium", "hard"],
            "current_difficulty": "easy"
        }
        
        # Initialize questions
        self._init_questions()
    
    def _init_questions(self):
        """Initialize the quiz questions with fun Python facts"""
        # Easy questions
        self.questions.extend([
            Question(
                "What keyword is used to define a function in Python?",
                "def",
                ["def", "function", "define", "func"],
                "easy"
            ),
            Question(
                "Which keyword is used for conditional statements?",
                "if",
                ["if", "when", "condition", "check"],
                "easy"
            ),
            Question(
                "What keyword represents the Boolean value 'true'?",
                "True",
                ["True", "true", "YES", "1"],
                "easy"
            ),
            Question(
                "Which keyword is used to exit a loop prematurely?",
                "break",
                ["break", "exit", "stop", "end"],
                "easy"
            ),
            Question(
                "Which symbol represents the 'and' operator in Python?",
                "and",
                ["and", "&&", "&", "+"],
                "easy"
            ),
            Question(
                "What was Python named after?",
                "Monty Python",
                ["Monty Python", "Snake", "Python's Triangle", "A person named Python"],
                "easy"
            )
        ])
        
        # Medium questions
        self.questions.extend([
            Question(
                "Which keyword is used to handle exceptions?",
                "try",
                ["try", "catch", "except", "handle"],
                "medium"
            ),
            Question(
                "What keyword is used to skip the current iteration in a loop?",
                "continue",
                ["continue", "skip", "next", "pass"],
                "medium"
            ),
            Question(
                "Which keyword represents 'nothing' in Python?",
                "None",
                ["None", "Null", "nil", "void"],
                "medium"
            ),
            Question(
                "What keyword is used to create a class?",
                "class",
                ["class", "struct", "object", "type"],
                "medium"
            ),
            Question(
                "Which keyword is used with 'try' to handle specific exceptions?",
                "except",
                ["except", "catch", "error", "handle"],
                "medium"
            ),
            Question(
                "Which built-in function converts a value to an integer?",
                "int()",
                ["int()", "integer()", "to_int()", "parse_int()"],
                "medium"
            )
        ])
        
        # Hard questions
        self.questions.extend([
            Question(
                "Which keyword creates anonymous functions?",
                "lambda",
                ["lambda", "anonymous", "function", "arrow"],
                "hard"
            ),
            Question(
                "What keyword allows a function to produce a series of values over time?",
                "yield",
                ["yield", "produce", "generate", "return"],
                "hard"
            ),
            Question(
                "Which keyword is used to work with global variables inside functions?",
                "global",
                ["global", "public", "extern", "shared"],
                "hard"
            ),
            Question(
                "What keyword is used for cleanup actions in exception handling?",
                "finally",
                ["finally", "cleanup", "end", "always"],
                "hard"
            ),
            Question(
                "Which keyword refers to variables in enclosing (but not global) scopes?",
                "nonlocal",
                ["nonlocal", "enclosed", "outer", "parent"],
                "hard"
            ),
            Question(
                "What is the name of Python's package manager?",
                "pip",
                ["pip", "pypm", "conda", "npm"],
                "hard"
            )
        ])
    
    def _clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _display_ascii_art(self):
        """Display a centered and larger Python Quiz title"""
        title = "🚀 PYTHON MASTERY QUIZ 🚀"
        print(title.center(50))  # Adjust the width as needed

    def welcome(self):
        """Display welcome message and get player name"""
        self._clear_screen()
        self._display_ascii_art()
        print("\n" + "=" * 50)
        print("\nTest your knowledge of Python keywords and concepts.")
        
        # Get player name
        while True:
            name = input("\nEnter your name: ").strip()
            if name:
                self.player_name = name
                break
            else:
                print("Please enter a valid name.")
        
        print(f"\nHello, {self.player_name}! Let's test your Python knowledge.")
        input("\nPress Enter to continue...")
        self._show_menu()
    
    def _show_menu(self):
        """Display the main menu"""
        while True:
            self._clear_screen()
            self._display_ascii_art()
            print("\n" + "=" * 50)
            print("MAIN MENU")
            print("=" * 50)
            print("1. Start New Quiz")
            print("2. Set Difficulty")
            print("3. View High Scores")
            print("4. Rules")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                input("\nPress Enter to start the quiz...")
                self.start_quiz()
            elif choice == "2":
                self._set_difficulty()
            elif choice == "3":
                self._show_high_scores()
            elif choice == "4":
                self._show_rules()
            elif choice == "5":
                self._exit_game()
                break
            else:
                print("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
    
    def _exit_game(self):
        """Exit the game with a nice farewell message"""
        self._clear_screen()
        
        farewell_message = f"""
        {self.player_name}, we're sad to see you go!
        
        Thanks for playing the Python Keyword Master Quiz!
        
        🐍 Hope you had fun and learned something new about Python 🐍
        
        Your final stats:
        - Highest score: {self._get_player_high_score()} points
        - Current difficulty: {self.config["current_difficulty"].capitalize()}
        
        Come back soon to test your Python knowledge again!
        """
        
        print(farewell_message)
        input("\nPress Enter to exit the game...")
        print("\nExiting game... Goodbye!")
    
    def _get_player_high_score(self):
        """Get the player's highest score"""
        player_scores = [score["best_score"] for score in self.high_scores 
                         if score["name"] == self.player_name]
        return max(player_scores) if player_scores else 0
    
    def _set_difficulty(self):
        """Set the quiz difficulty"""
        self._clear_screen()
        print("\n" + "=" * 50)
        print("SET DIFFICULTY")
        print("=" * 50)
        print("1. Easy - Perfect for beginners!")
        print("2. Medium - For those who know their Python basics.")
        print("3. Hard - Only for Python masters!")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            self.config["current_difficulty"] = "easy"
            print("Difficulty set to Easy. You'll get basic Python questions.")
        elif choice == "2":
            self.config["current_difficulty"] = "medium"
            print("Difficulty set to Medium. Prepare for some challenges!")
        elif choice == "3":
            self.config["current_difficulty"] = "hard"
            print("Difficulty set to Hard. Good luck, Python master!")
        else:
            print("Invalid choice. Keeping current difficulty.")
        
        input("\nPress Enter to continue...")
    
    def _show_high_scores(self):
        """Show the high scores with attempts tracking"""
        self._clear_screen()
        print("\n" + "=" * 50)
        print("HIGH SCORES")
        print("=" * 50)
        
        if not self.high_scores:
            print("No high scores yet. Be the first!")
            input("\nPress Enter to continue...")
            return
        
        # Sort high scores by best score (descending)
        sorted_scores = sorted(self.high_scores, 
                                key=lambda x: x.get('best_score', 0), 
                                reverse=True)
        
        print("\nRANK | NAME               | BEST | LAST | ATTEMPTS | DIFFICULTY | DATE")
        print("-" * 80)
        
        for idx, entry in enumerate(sorted_scores, 1):
            name_display = entry['name'][:18] + '...' if len(entry['name']) > 18 else entry['name'].ljust(18)
            print(f"{idx:4} | {name_display} | {entry.get('best_score', 0):4} | {entry.get('last_score', 0):4} | {entry.get('attempts', 1):8} | {entry['difficulty'].ljust(10)} | {entry['date']}")
        
        input("\nPress Enter to continue...")
    
    def _show_rules(self):
        """Show the game rules"""
        self._clear_screen()
        print("\n" + "=" * 50)
        print("RULES")
        print("=" * 50)
        print("1. You'll be presented with multiple-choice questions about Python.")
        print(f"2. You have {self.config['time_limit']} seconds to answer each question.")
        print("3. Each correct answer earns you points based on difficulty:")
        print("   - Easy: 1 point")
        print("   - Medium: 2 points")
        print("   - Hard: 3 points")
        print("4. There's no penalty for wrong answers.")
        print("5. Try to get the highest score possible!")
        print("6. Have fun while learning about Python!")
        
        input("\nPress Enter to continue...")
    
    def _get_fun_fact(self):
        """Return a random fun fact about Python"""
        facts = [
            "The Python language was named after Monty Python, not the snake!",
            "Python was created by Guido van Rossum in the late 1980s.",
            "Python's design philosophy emphasizes code readability with its notable use of whitespace.",
            "Python consistently ranks as one of the most popular programming languages worldwide.",
            "The Zen of Python contains 19 'guiding principles' for writing computer programs in Python.",
            "Python has been used to create popular applications like Instagram, Spotify, and Dropbox.",
            "You can type 'import this' in Python to see the Zen of Python!",
            "There are over 137,000 Python libraries available for various tasks.",
            "Python can be used for web development, data analysis, AI, scientific computing, and more!",
            "Python's mascot is a pair of snakes named 'Python' and 'Monty'."
        ]
        return random.choice(facts)
    
    def start_quiz(self):
        """Start a new quiz"""
        # Reset score
        self.score = 0
        
        # Filter questions by current difficulty
        current_diff = self.config["current_difficulty"]
        
        # Get all questions for current difficulty and below
        available_difficulties = []
        if current_diff == "easy":
            available_difficulties = ["easy"]
        elif current_diff == "medium":
            available_difficulties = ["easy", "medium"]
        else:  # hard
            available_difficulties = ["easy", "medium", "hard"]
        
        filtered_questions = [q for q in self.questions if q.difficulty in available_difficulties]
        
        # Shuffle questions
        random.shuffle(filtered_questions)
        
        # Select a subset of questions
        self.total_questions = min(10, len(filtered_questions))
        selected_questions = filtered_questions[:self.total_questions]
        
        self._clear_screen()
        print("\n" + "=" * 50)
        print(f"STARTING QUIZ - {current_diff.upper()} DIFFICULTY")
        print("=" * 50)
        print(f"You'll have {self.total_questions} questions to answer.")
        print(f"\nFun fact: {self._get_fun_fact()}")
        
        input("\nPress Enter when you're ready to start...")
        
        # Loop through questions
        for i, question in enumerate(selected_questions, 1):
            self.current_question = question
            
            self._clear_screen()
            # Display the question
            print(f"\nQuestion {i}/{self.total_questions}")
            print("-" * 30)
            print(question.text)
            
            # Display options
            options = question.options.copy()
            random.shuffle(options)
            
            for idx, option in enumerate(options, 1):
                print(f"{idx}. {option}")
            
            # Start timer
            start_time = time.time()
            time_is_up = False
            
            # Get user answer with timeout
            answer = None
            while True:
                # Check if time is up
                if time.time() - start_time > self.config["time_limit"]:
                    time_is_up = True
                    break
                
                # Display time remaining every 5 seconds
                time_elapsed = time.time() - start_time
                time_remaining = max(0, self.config["time_limit"] - time_elapsed)
                
                user_input = input(f"\nYour answer (1-4) [{time_remaining:.0f}s remaining]: ")
                
                if user_input.strip() and user_input in "1234":
                    answer = options[int(user_input) - 1]
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")
            
            # Handle timeout
            if time_is_up:
                print("\nTime's up! Moving to the next question.")
                print(f"The correct answer was: {question.answer}")
                input("\nPress Enter to continue...")
                continue
            
            # Check answer
            if answer == question.answer:
                # Award points based on difficulty
                points = 1  # easy
                if question.difficulty == "medium":
                    points = 2
                elif question.difficulty == "hard":
                    points = 3
                
                self.score += points
                print(f"\n🎉 Correct! You earned {points} point(s).")
                print(f"Current score: {self.score}")
            else:
                print(f"\n❌ Wrong! The correct answer was: {question.answer}")
            
            # Show a random encouragement after each question
            encouragements = [
                "Keep going! You're doing great!",
                "You've got this!",
                "You're on fire!",
                "Python masters are made, not born!",
                "Knowledge is power!",
                "Every question makes you stronger!"
            ]
            print(f"\n{random.choice(encouragements)}")
            
            # Pause before next question
            input("\nPress Enter for the next question...")
        
        # Quiz finished
        self._end_quiz()
    
    def _end_quiz(self):
        """End the quiz and show results"""
        self._clear_screen()
        print("\n" + "=" * 50)
        print("🎮 QUIZ COMPLETED! 🎮")
        print("=" * 50)
        print(f"Your final score: {self.score} points")
        
        # Calculate max possible score
        max_score = self.total_questions
        if self.config["current_difficulty"] == "medium":
            max_score = self.total_questions * 2
        elif self.config["current_difficulty"] == "hard":
            max_score = self.total_questions * 3
        
        percentage = (self.score / max_score) * 100
        print(f"You got {percentage:.1f}% of the maximum possible score.")
        
        # Evaluate performance
        if percentage >= 90:
            print("\n🏆 Excellent! You're a Python master! 🏆")
            print("Your Python knowledge is truly impressive!")
        elif percentage >= 70:
            print("\n🌟 Great job! You know your Python well. 🌟")
            print("You've got solid Python knowledge!")
        elif percentage >= 50:
            print("\n👍 Good effort! Keep learning. 👍")
            print("You're on your way to becoming a Python expert!")
        else:
            print("\n📚 Keep practicing your Python knowledge. 📚")
            print("Every master was once a beginner!")
        
        # Track quiz attempts
        player_attempts = next((entry for entry in self.high_scores 
                                if entry['name'] == self.player_name), None)
        
        if player_attempts:
            # Increment attempts for existing player
            player_attempts['attempts'] = player_attempts.get('attempts', 1) + 1
            player_attempts['best_score'] = max(player_attempts.get('best_score', 0), self.score)
            player_attempts['last_score'] = self.score
            
            # Update existing entry
            for i, entry in enumerate(self.high_scores):
                if entry['name'] == self.player_name:
                    self.high_scores[i] = player_attempts
                    break
        else:
            # Add new player entry with attempts
            self.high_scores.append({
                "name": self.player_name,
                "score": self.score,
                "best_score": self.score,
                "last_score": self.score,
                "attempts": 1,
                "difficulty": self.config["current_difficulty"],
                "date": time.strftime("%Y-%m-%d")
            })
        
        # Save high scores
        try:
            with open("high_scores.json", "w") as f:
                json.dump(self.high_scores, f)
            print("\nYour score has been saved to the high scores!")
        except:
            print("\nCould not save high score.")
        
        # Ask if they want to play again
        print("\nWould you like to play again?")
        print("1. Yes, let's play another round!")
        print("2. No, return to main menu")
        
        while True:
            choice = input("\nEnter your choice (1-2): ")
            if choice == "1":
                self.start_quiz()
                break
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")
        
        # If they chose not to play again, we return to the main menu

class NewPlayer:
    """Class to handle new player creation"""
    @staticmethod
    def create_new_player():
        """Create a new player and start the game"""
        game = QuizGame()
        game.welcome()

# Run the game when script is executed
if __name__ == "__main__":
    # Create a new player instance
    new_player = NewPlayer()
    new_player.create_new_player()