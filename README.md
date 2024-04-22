# footlang

<img src="./ebnf.png" width="100%">

ebnf 
```
program = { statement };

statement = action_statement | decision | loop | assignment;

action_statement = identifier, action, '(', [ identifier ], ')', ';';
action = 'pass' | 'move';

decision = 'decide', '(', expression, ')', '{', { statement }, '}', 'otherwise', '{', { statement }, '}';

loop = 'repeat', '(', expression, ')', '{', { statement }, '}';

assignment = identifier, '=', expression, ';';

expression = identifier | number | property_access | function_call;
property_access = identifier, '.', property;
property = 'energy';
function_call = 'distance', '(', identifier, ',', identifier, ')';
comparison_operator = '>' | '<' | '==' | '!=';

identifier = letter, { letter | digit };
number = digit, { digit };
letter = 'a' | '...' | 'Z';
digit = '0' | '...' | '9';

```

## Example
```
player1;
player2;
newPosition = 30;

decide (distance(player1, player2) < 10) {
    player1.pass(player2);
} otherwise {
    player1.move(newPosition);
}

repeat (player1.energy > 50) {
    player1.pass(player2);
    player1.energy = player1.energy - 5;
}
```
