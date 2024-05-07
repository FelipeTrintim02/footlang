# footlang

<img src="./ebnf.png" width="100%">

ebnf 
```
program = { statement };

statement = assignment | loop | decision | block ;

assignment = identifier, "=", expression, ";" ;

loop = "repeat", "(", expression, ")", block ;

decision = "decide", "(", expression, ")", block, ["otherwise", block] ;

block = "{", { statement }, "}" ;

expression = term, { ("+" | "-"), term };

term = factor, { ("*" | "/"), factor };

factor = integer 
       | identifier 
       | "(", expression, ")";

integer = [ "-" ], digit, { digit };

identifier = letter, { letter | digit | "." };

relational_operator = ">" | "<" | "==" | "!=" | ">=" | "<=" ;

letter = "a" | "..." | "z" | "A" | "..." | "Z";
digit = "0" | "..." | "9";
```

## Example
```
player.energy = 100;
player.positionx = 0;
player.positiony = 0;

repeat (player.energy > 20) {
    player.energy = player.energy - 20;
    player.positionx = player.positionx + 10;
    decide (player.positionx > 100) {
        player.positionx = 0;
        player.positiony = player.positiony + 10;
    }
    otherwise {
        player.positionx = player.positionx + 10;
    }
}

```

## Example2
```
player1.energy = 100;
player2.energy = 100;
player1.positionx = 0;
player2.positionx = 50;

repeat (player1.energy > 20) {
    player1.positionx = player1.positionx + 5;
    player2.positionx = player2.positionx - 5;
    player1.energy = player1.energy - 10;
    player2.energy = player2.energy - 10;

    decide (player1.positionx > player2.positionx) {
        decide (player1.energy < 30) {
            player1.energy = player1.energy + 20;
        }
        otherwise {
            player1.energy = player1.energy - 5;
        }
    }
    otherwise {
        decide (player2.energy < 30) {
            player2.energy = player2.energy + 20;
        }
        otherwise {
            player2.energy = player2.energy - 5;
        }
    }
}
```