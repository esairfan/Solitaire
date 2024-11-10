# Solitaire Game

A digital implementation of the classic Solitaire card game developed using Python and Pygame. The goal is to move all cards from the tableau to the foundation piles by following traditional Solitaire rules.

## Features

- *Classic Gameplay*: Move cards between tableau columns and foundation piles to complete the game.
- *Tableau and Foundation*: Seven tableau columns and four foundation piles.
- *Stock and Waste Piles*: Draw cards from the stock to the waste and move them to tableau or foundation.
- *Scoring and Time System*: Tracks your score and game duration.
- *Moves Counter*: Displays the number of moves made.
- *Mission System*: Additional objectives, such as scoring points and moving specific cards within limited moves.
- *Red Sequence Tracking*: Counts red cards moved in a specific sequence to foundation.
- *Graphical Interface*: Built with Pygame, featuring interactive cards and an attractive background.

## Game Rules

1. *Objective*: Move all cards to the foundation piles in ascending order by suit.
2. *Tableau Rules*:
   - Cards must alternate in color and follow descending order.
   - Only the top card in each column is movable.
3. *Foundation Rules*:
   - Each pile must be filled from Ace to King in the same suit.
4. *Stock and Waste Piles*:
   - Cards drawn from the stock pile move to the waste pile.
5. *Win Condition*: Game ends when all foundation piles are completed in the correct order.

## Classes and Structure

- *Card*: Manages attributes like suit, rank, and display.
- *Deck*: Shuffles and deals cards.
- *Foundation*: Handles the piles for each suit in ascending order.
- *Tableau*: Manages columns where cards can be moved according to Solitaire rules.
- *Stock and Waste*: Handles drawing and cycling of cards.
- *Mission*: Tracks extra challenges during gameplay.

## User Interface

- *Game Window*: Displays tableau columns, foundations, stock, and waste pile.
- *Interactive Elements*: Start, pause, and mission displays, along with score and moves counter.
- *Graphical Interface*: Cards are animated, and the game has a visually engaging background.

## Controls

- *Click and Drag*: Move cards between tableau and foundation piles.
- *Escape*: Pause the game.

## Mission List

- *Score 200 points*: Reach a score of 200.
- *Move all four aces within 30 moves*: Move all aces to the foundation early.
- *Empty stock and waste piles*: Remove all cards from these piles.

## Future Enhancements

- Additional missions and levels of difficulty.
- Enhanced sound effects and animations.

## Contact

For questions, suggestions, or issues, please contact the developer:

- *Email*: [ibrahimirfan815@gmail.com](mailto:ibrahimirfan815@gmail.com)
- *GitHub*: [github.com/esairfan](https://github.com/esairfan)
- *LinkedIn*: [linkedin.com/in/esa-irfan-902108295](https://www.linkedin.com/in/esa-irfan-902108295)

Feel free to reach out with any feedback or ideas for future enhancements!
## Installation

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/esairfan/cse200m24pid104.git
   
2. Install dependencies:
   ```bash
   pip install pygame

3.Run the Game 
   ```bash
   python solitaire.py

