# footlang

<img src="./ebnf.png" width="100%">

ebnf

```
program = { statement };

statement = assignment | loop | decision | block | winner_statement ;

assignment = identifier, "=", expression, ";" ;

loop = "repeat", "(", expression, ")", block ;

decision = "decide", "(", expression, ")", block, ["otherwise", block] ;

block = "{", { statement }, "}" ;

expression = term, { ("+" | "-" | "*" | "/" | ">" | "<" | "==" | "!=" | ">=" | "<=" | "&&" | "||" | ".."), term };

term = factor ;

factor = integer
       | identifier
       | "(", expression, ")" ;

integer = [ "-" ], digit, { digit } ;

identifier = predefined_identifier ;

predefined_identifier = identifier, ".", ("velocity" | "energy") ;

winner_statement = "winner", "(", (string | identifier), ")", ";" ;

string = '"', { letter | digit | " " }, '"' ;

letter = "a" | "..." | "z" | "A" | "..." | "Z" ;
digit = "0" | "..." | "9" ;



```

## Example

```
runner1.energy = 100;
runner2.energy = 100;
runner1.velocity = 0;
runner2.velocity = 0;

repeat (runner1.energy > 20 && runner2.energy > 20) {
    runner1.velocity = runner1.velocity + 10;
    runner2.velocity = runner2.velocity + 8;
    runner1.energy = runner1.energy - 15;
    runner2.energy = runner2.energy - 12;

    decide (runner1.velocity > 100) {
        winner("Runner 1 wins!");
    }
    otherwise {
        decide (runner2.velocity > 100) {
            winner("Runner 2 wins!");
        }
    }
}

winner("Race ended!");

```

## Example

```
runner1.energy = 100;
runner2.energy = 100;
runner1.velocity = 5;
runner2.velocity = 5;

volta = 1;
tempo = 0;

repeat (volta < 10) {
    runner1.energy = runner1.energy - 10;
    runner2.energy = runner2.energy - 10;
    
    tempo = tempo + 1;

    winner("volta: ");
    winner(volta);

    decide (runner1.energy > 50) {
        runner1.velocity = runner1.velocity + 1;
    }
    decide (runner2.energy > 50) {
        runner2.velocity = runner2.velocity + 2;
    }

    decide (runner1.energy == 0 || runner2.energy == 0) {
        winner("Um dos corredores está sem energia!");
        winner("Corrida interrompida!");
        volta = 10; 
    }

    volta = volta + 1;

    winner(" ");
}

distancia1 = runner1.velocity * tempo;
distancia2 = runner2.velocity * tempo;

winner("chegada");

decide (distancia1 > distancia2) {
    winner("Runner1 é o campeão! Distância: ");
    winner(distancia1);
    winner(" metros, Tempo: ");
    winner(tempo);
    winner("segundos");
} otherwise {
    winner("Runner2 é o campeão! Distância: ");
    winner(distancia2);
    winner(" metros, Tempo: ");
    winner(tempo);
    winner("segundos");
}
```