# Lexer: it reads the input of characters and convert them into a stream of tokens

#--------CONSTANTS--------#

DIGITS = '0123456789'
INT = 'INT'
FLOAT = 'FLOAT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'

#--------ERROR--------#

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}:{self.details}'
        result += f'\nFile {self.pos_start.fn}, lne{self.pos_start.r+1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#--------POSITION--------#

class Position:
    def __init__(self, idx, r, c, fn, ftxt):
        self.idx = idx
        self.r = r
        self.c = c
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx+=1
        self.c+=1

        if current_char=="\n":
            self.r+=1
            self.c=0

        return self
    
    def copy(self):
        return Position(self.idx, self.r, self.c, self.fn, self.ftxt)

#--------TOKEN--------#

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#--------LEXER--------#

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx<len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char!=None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_num())
            elif self.current_char =='+':
                tokens.append(Token(PLUS))
                self.advance()
            elif self.current_char =='-':
                tokens.append(Token(MINUS))
                self.advance()
            elif self.current_char =='*':
                tokens.append(Token(MUL))
                self.advance()
            elif self.current_char =='/':
                tokens.append(Token(DIV))
                self.advance()
            elif self.current_char =='(':
                tokens.append(Token(LPAREN))
                self.advance()
            elif self.current_char ==')':
                tokens.append(Token(RPAREN))
                self.advance()                
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'"+char+"'")
        return tokens, None
    
    def make_num(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS+'.':
            if self.current_char =='.':
                if dot_count==1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(INT, int(num_str))
        else:
            return Token(FLOAT, float(num_str))
        
#--------RUN--------#

def run(file_name, text):
    lex = Lexer(file_name, text)
    tokens, error = lex.make_tokens()

    return tokens, error

