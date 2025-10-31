const boxGrid = document.getElementById('boxGrid');
const guessInput = document.getElementById('guessInput');
const guessButton = document.getElementById('guessButton');

async function fetchWords(url) {

    const lines = data.split('\n');
    const headers = lines[0].split(',');
    return lines.slice(1).map(line => {
    const values = line.split(',');
    return headers.reduce((obj, header, index) => {
      obj[header] = values[index];
      return obj;
      }, {});
    });

    const csvData = await readCSV(url);
    const parsedData = parseCSV(csvData);
    console.log(parsedData);
  }

function parseWords(data) {

}

async function fetchAndParseWords(url) {
    const csvData = await readCSV(url);
    const parsedData = parseCSV(csvData);
    console.log(parsedData);
}

/** 
    let wordList = [];
    try {
        const response = await fetch(url, { method: 'get'});
        const data = await response.text();
        wordList = data.split("\n");
    } catch (error) {
        console.error('Error fetching CSV:', error);
    }
    console.log(wordList);
    return wordList;
}*/

class Game {
    constructor() {
      // pick word
      (async () => {(this.words = await fetchWords('5_letter_words.csv'))})()

      console.log(this.words);
      this.i = Math.floor(Math.random() * 496); // number of possible words
      this.answer = this.words[this.i];
      console.log(this.answer);
      this.answer = 'ARISE';
      
      // make 6x5 grid of boxes
      this.boxes = [];
      this.makeGrid();
      this.row = 0; // current row

      this.guess = '';

      this.message_on = false; // true if msg on screen
      this.over = false; // true if the game is over
      this.won = false;


    }

    handleEvent (event) {
		  this.updateGrid();
	  } 


    initGame() {
      // Event listener for the guess button
      guessButton.addEventListener('click', this);
    }
  
    isWordValid() {
        let guess = guessInput.value.toUpperCase();
        if (guess.length === 5) {
          if (Array.from(guess).every((char) =>/[A-Za-z]/.test(char))) {
            //if (Array.from(this.words).includes(guess)) {
                this.guess = guess;
                guessInput.value = "";
            //} else {
            //  alert('Your guess is not on the list of possible words.')
            //  return false;
            //}
          } else {
            alert('Please use alphabetic letters only.')
            return false;
          }
        } else {
            alert('Please enter a 5-letter word.');
            return false;
        }
      return true;
    }

    // determines which letters are correct
    updateGrid() {
      if (this.isWordValid()) {
      let numCorrect = 0; 
      let color = '';
      for (let y = 0; y < 5; y++) { // # of cols
          if (this.guess[y] === this.answer[y]) {
              color = 'green';
              numCorrect += 1;
          } else if (this.answer.includes(this.guess[y])) {
              color = 'yellow';
          } else {
              color = 'grey';
          }
          this.boxes[this.row][y].color = color;
          this.boxes[this.row][y].letter = this.guess[y];
          
          this.boxes[this.row][y].box.textContent = this.guess[y];
          this.boxes[this.row][y].box.classList.add(color);
      }

      if (numCorrect === 5) {
        this.over = true;
        this.won = true;
      } else {
        if (this.row < 6) {
          this.row += 1 // move on to next row
      } else {
          this.over = true;
          this.won = false;
        }
      }

      if (this.row < 6) {
          this.row += 1 // move on to next row
      } 
    }
    }

    makeGrid() {
      for (let x = 0; x < 6; x++) { // # of rows
          this.boxes[x] = [];
          for (let y = 0; y < 5; y++) { // # of cols
              // create box and add to boxes list
              this.boxes[x][y] = new Box(x, y)
          }
      }
    }

}

class Box {
  constructor(x, y) {
    this.x = x
    this.y = y
    this.letter = '';
    this.color = '';
    this.box = document.createElement('div');
    this.box.classList.add('box');
    boxGrid.appendChild(this.box);
  }
}

let game = new Game();
game.initGame();

/**Display Area for Feedback
Adding Animations and Transitions

Animations can make your game feel more dynamic. We'll add some smooth transitions to make the gameplay experience even more engaging.
User Feedback and Error Handling

A great game communicates with its players. We'll implement clear messages for errors and successes, enhancing the overall user experience.
Storing Game Data
Using Local Storage for Game Progress

Don't want players to lose their progress? We'll use the browser's local storage to save their game state, so they can pick up where they left off.
Reset and Continue Game Options

Giving players the option to reset or continue their game is key. We'll add functionality for both, making your game flexible and user-friendly.
Making the Game Challenging
Implementing a Dictionary of Words

A good Wordle game needs a solid word list. We'll explore how to implement a dictionary of words that the game can use to challenge players.
Difficulty Levels and Daily Challenges

To keep things spicy, we'll add different difficulty levels and daily challenges. This will keep your players coming back for more.
**/