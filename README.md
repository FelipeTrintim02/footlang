# footlang

<img src="./ebnf.png" width="100%">

ebnf 
```
program = { statement };

statement = action_statement | decision | loop;

action_statement = identifier, action, '(', [ identifier ], ')', ';';
action = 'pass' | 'move';

decision = 'decide', '(', condition, ')', '{', { statement }, '}', 'otherwise', '{', { statement }, '}';

loop = 'repeat', '(', condition, ')', '{', { statement }, '}';

condition = expression, comparison_operator, expression;
expression = identifier | number;
comparison_operator = '>' | '<' | '==' | '!=';

identifier = letter, { letter | digit };
number = digit, { digit };
letter = 'a' |'... '|'z' | 'A' |'...'| 'Z';
digit = '0' | '...' | '9';
```