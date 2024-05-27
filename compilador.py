import re
import sys

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class PrePro:
    @staticmethod
    def filter(expression):
        return re.sub(r'--.*', '', expression)

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.reserved = ['repeat', 'decide', 'otherwise', 'winner', 'velocity', 'energy']

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF', None)
        elif self.source[self.position].isdigit():
            number = ''
            while self.position < len(self.source) and self.source[self.position].isdigit():
                number += self.source[self.position]
                self.position += 1
            self.next = Token('INTEGER', int(number))
        elif self.source[self.position].isalpha() or self.source[self.position] == "_":
            identifier = ''
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "." or self.source[self.position] == "_"):
                identifier += self.source[self.position]
                self.position += 1
            if identifier in self.reserved:
                self.next = Token(identifier.upper(), None)
            else:
                self.next = Token('IDENTIFIER', identifier)
        elif self.source[self.position] == "=":
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                self.next = Token("EQ", None)
                self.position += 2
            else:
                self.next = Token("ASSIGN", None)
                self.position += 1
        elif self.source[self.position] == "+":
            self.next = Token("PLUS", None)
            self.position += 1
        elif self.source[self.position] == "-":
            self.next = Token("MINUS", None)
            self.position += 1
        elif self.source[self.position] == "*":
            self.next = Token("MULT", None)
            self.position += 1
        elif self.source[self.position] == "/":
            self.next = Token("DIV", None)
            self.position += 1
        elif self.source[self.position] == "(":
            self.next = Token("LPAREN", None)
            self.position += 1
        elif self.source[self.position] == ")":
            self.next = Token("RPAREN", None)
            self.position += 1
        elif self.source[self.position] == "{":
            self.next = Token("LBRACE", None)
            self.position += 1
        elif self.source[self.position] == "}":
            self.next = Token("RBRACE", None)
            self.position += 1
        elif self.source[self.position] == ">":
            self.next = Token("GT", None)
            self.position += 1
        elif self.source[self.position] == "<":
            self.next = Token("LT", None)
            self.position += 1
        elif self.source[self.position] == ";":
            self.next = Token("SEMI", None)
            self.position += 1
        elif self.source[self.position] == "&" and self.position + 1 < len(self.source) and self.source[self.position + 1] == "&":
            self.position += 2
            self.next = Token("AND", None)
        elif self.source[self.position] == "|" and self.position + 1 < len(self.source) and self.source[self.position + 1] == "|":
            self.position += 2
            self.next = Token("OR", None)
        elif self.source[self.position] == "\"":
            self.position += 1
            string_literal = ''
            while self.position < len(self.source):
                if self.source[self.position] == "\\":
                    self.position += 1
                    if self.position < len(self.source) and self.source[self.position] in "\"nt":
                        if self.source[self.position] == "\"":
                            string_literal += "\""
                        elif self.source[self.position] == "n":
                            string_literal += "\n"
                        elif self.source[self.position] == "t":
                            string_literal += "\t"
                elif self.source[self.position] == "\"":
                    self.position += 1
                    break
                else:
                    string_literal += self.source[self.position]
                self.position += 1
            self.next = Token('STRING', string_literal)
        elif self.source[self.position] == ",":
            self.next = Token("COMMA", None)
            self.position += 1
        else:
            sys.stderr.write(f"Unexpected character: {self.source[self.position]}\n")
            sys.exit(1)

class SymbolTable:
    def __init__(self):
        self.table = {}

    def setter(self, key, value):
        self.table[key] = value

    def getter(self, key):
        if key in self.table:
            return self.table[key]
        else:
            raise ValueError(f"Variable {key} not declared")

class Node:
    def evaluate(self, st):
        pass

class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, st):
        for statement in self.statements:
            statement.evaluate(st)

class AssignmentNode(Node):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr

    def evaluate(self, st):
        st.setter(self.identifier, self.expr.evaluate(st))

class LoopNode(Node):
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block

    def evaluate(self, st):
        while self.expr.evaluate(st):
            self.block.evaluate(st)

class DecisionNode(Node):
    def __init__(self, expr, if_block, else_block):
        self.expr = expr
        self.if_block = if_block
        self.else_block = else_block

    def evaluate(self, st):
        if self.expr.evaluate(st):
            self.if_block.evaluate(st)
        elif self.else_block:
            self.else_block.evaluate(st)

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, st):
        for statement in self.statements:
            statement.evaluate(st)

class WinnerNode(Node):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, st):
        value = self.expr.evaluate(st)
        print(value)

class IntegerNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return self.value

class IdentifierNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return st.getter(self.value)

class StringNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return self.value

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        left = self.children[0].evaluate(st)
        right = self.children[1].evaluate(st)

        if self.value == 'PLUS':
            return left + right
        elif self.value == 'MINUS':
            return left - right
        elif self.value == 'MULT':
            return left * right
        elif self.value == 'DIV':
            return left // right
        elif self.value == 'GT':
            return left > right
        elif self.value == 'LT':
            return left < right
        elif self.value == 'EQ':
            return left == right
        elif self.value == 'AND':
            return left and right
        elif self.value == 'OR':
            return left or right
        else:
            raise ValueError(f"Unknown binary operator: {self.value}")

class Parser:
    tokens = None

    @staticmethod
    def parse(tokens):
        Parser.tokens = tokens
        return Parser.parse_program()

    @staticmethod
    def parse_program():
        statements = []
        while Parser.tokens[0].type != 'EOF':
            statements.append(Parser.parse_statement())
        return ProgramNode(statements)

    @staticmethod
    def parse_statement():
        if Parser.tokens[0].type == 'IDENTIFIER':
            return Parser.parse_assignment()
        elif Parser.tokens[0].type == 'REPEAT':
            return Parser.parse_loop()
        elif Parser.tokens[0].type == 'DECIDE':
            return Parser.parse_decision()
        elif Parser.tokens[0].type == 'LBRACE':
            return Parser.parse_block()
        elif Parser.tokens[0].type == 'WINNER':
            return Parser.parse_winner_statement()
        else:
            raise Exception(f"Unexpected token {Parser.tokens[0].type}")

    @staticmethod
    def parse_assignment():
        identifier = Parser.tokens.pop(0).value
        if Parser.tokens.pop(0).type != 'ASSIGN':
            raise Exception("Expected '='")
        expr = Parser.parse_expression()
        if Parser.tokens.pop(0).type != 'SEMI':
            raise Exception("Expected ';'")
        return AssignmentNode(identifier, expr)

    @staticmethod
    def parse_loop():
        Parser.tokens.pop(0)  # 'repeat'
        if Parser.tokens.pop(0).type != 'LPAREN':
            raise Exception("Expected '('")
        expr = Parser.parse_expression()
        if Parser.tokens.pop(0).type != 'RPAREN':
            raise Exception("Expected ')'")
        block = Parser.parse_block()
        return LoopNode(expr, block)

    @staticmethod
    def parse_decision():
        Parser.tokens.pop(0)  # 'decide'
        if Parser.tokens.pop(0).type != 'LPAREN':
            raise Exception("Expected '('")
        expr = Parser.parse_expression()
        if Parser.tokens.pop(0).type != 'RPAREN':
            raise Exception("Expected ')'")
        if_block = Parser.parse_block()
        else_block = None
        if Parser.tokens[0].type == 'OTHERWISE':
            Parser.tokens.pop(0)
            else_block = Parser.parse_block()
        return DecisionNode(expr, if_block, else_block)

    @staticmethod
    def parse_block():
        if Parser.tokens.pop(0).type != 'LBRACE':
            raise Exception("Expected '{'")
        statements = []
        while Parser.tokens[0].type != 'RBRACE':
            statements.append(Parser.parse_statement())
        Parser.tokens.pop(0)  # '}'
        return BlockNode(statements)

    @staticmethod
    def parse_winner_statement():
        Parser.tokens.pop(0)  # 'winner'
        if Parser.tokens.pop(0).type != 'LPAREN':
            raise Exception("Expected '('")
        if Parser.tokens[0].type == 'STRING':
            expr = StringNode(Parser.tokens.pop(0).value)
        elif Parser.tokens[0].type == 'IDENTIFIER':
            expr = IdentifierNode(Parser.tokens.pop(0).value)
        else:
            raise Exception("Expected string or identifier")
        if Parser.tokens.pop(0).type != 'RPAREN':
            raise Exception("Expected ')'")
        if Parser.tokens.pop(0).type != 'SEMI':
            raise Exception("Expected ';'")
        return WinnerNode(expr)

    @staticmethod
    def parse_expression():
        result = Parser.parse_term()
        while Parser.tokens[0].type in ('PLUS', 'MINUS', 'GT', 'LT', 'EQ', 'AND', 'OR'):
            op = Parser.tokens.pop(0).type
            result = BinOp(op, [result, Parser.parse_term()])
        return result

    @staticmethod
    def parse_term():
        return Parser.parse_factor()

    @staticmethod
    def parse_factor():
        if Parser.tokens[0].type == 'INTEGER':
            return IntegerNode(Parser.tokens.pop(0).value)
        elif Parser.tokens[0].type == 'IDENTIFIER':
            return IdentifierNode(Parser.tokens.pop(0).value)
        elif Parser.tokens[0].type == 'STRING':
            return StringNode(Parser.tokens.pop(0).value)
        elif Parser.tokens[0].type == 'LPAREN':
            Parser.tokens.pop(0)  # '('
            expr = Parser.parse_expression()
            if Parser.tokens.pop(0).type != 'RPAREN':
                raise Exception("Expected ')'")
            return expr
        else:
            raise Exception(f"Unexpected token {Parser.tokens[0].type}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python main.py <filename>\n")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            code = file.read()
        st = SymbolTable()
        code = PrePro.filter(code)
        tokenizer = Tokenizer(code)
        tokens = []
        tokenizer.selectNext()
        while tokenizer.next.type != 'EOF':
            tokens.append(tokenizer.next)
            tokenizer.selectNext()
        tokens.append(tokenizer.next)  # Add the EOF token
        ast = Parser.parse(tokens)
        ast.evaluate(st)
    except FileNotFoundError:
        sys.stderr.write(f"Error: File {filename} not found\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)
