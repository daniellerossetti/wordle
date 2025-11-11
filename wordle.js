const boxGrid = document.getElementById('boxGrid');
const guessInput = document.getElementById('guessInput');
const guessButton = document.getElementById('guessButton');

async function fetchWords(url) {
    try {
        const response = await fetch(url);
        const data = await response.text();
        document.getElementById('output').innerText = data;
        return data;
    } catch (error) {
          console.error('Error in fetchWords:', error);
    }
    
    Papa.parse(url, {
        header: true,
        complete: function(results) {
            document.getElementById('output').innerText = JSON.stringify(results.data, null, 2);
        },
        error: function(error) {
            console.error('Error in fetchWords:', error);
        }
    });
    
}

/** Game class and Box class
    is Box class necessary?
    #1 - start game - event listener for the guess button
    #2 - pick word
        fetch words
        parse words
        pick an index
    #3 - make 6x5 grid of boxes
        create 6x5 boxes and put them on a list
    #4 - handle event -> check if word valid
    #5 - update grid
        update boxes color
        update guess 
 **/

class Game {
    constructor() {
      // pick word
      fetchWords('5_letter_words.csv');
      const results = document.getElementById('output').innerText.split("\n");
      console.log(results);
      const i = Math.floor(Math.random() * 496); // number of possible words
      const answer = results[i];

      console.log(answer);
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



async function main(){
    let game = new Game();
    game.initGame();
}
main().catch(console.log);
