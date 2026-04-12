import argparse
import os
import sys
from dataclasses import dataclass
from token_types import TokenType
from reader import Reader

c_types = {"int", "float", "char"}
c_punctuators = {'{','}', '(', ')', '[', ']', ';'}
c_keywords = {'return'}
c_functions = {'printf'}

@dataclass(frozen=True, slots=True)
class Token:
  token_type: TokenType
  token_value: str
  starting_pos: int
  ending_pos: int
  
type TokenList = list[Token]

class Lexer:
  def __init__(self):
    self.token_list: TokenList = []
  
  def parse_code(self, content:str) -> TokenList:
    reader = Reader(content)
    
    while not reader.at_end():
      char = reader.peek()

      if char.isspace():
        reader.advance()
      elif char == '"':
        self.token_list.append(self.handle_string(reader))
      elif char.isalpha():
        self.token_list.append(self.handle_word(reader))
      elif char.isdigit():
        self.token_list.append(self.handle_numbers(reader))
      elif not char.isalpha() and not char.isdigit():
        self.token_list.append(self.handle_symbols(reader))
         
    return self.token_list
    
  def handle_string(self, reader: Reader):
    start_index = reader.current_index
    
    reader.advance()
    
    while not reader.at_end() and not reader.peek() == '"':
      reader.advance()
    
    word = reader.content[start_index:reader.current_index + 1]
    reader.advance()
    
    return Token(TokenType.STRING_LITERAL, word, start_index, reader.current_index)
      
  def handle_word(self, reader: Reader):
    start_index = reader.current_index
    
    while not reader.at_end() and reader.peek().isalpha():
      reader.advance()
      
    word = reader.content[start_index:reader.current_index]
    
    token_type = None
    
    match word:
      case _ if word in c_types:
        token_type = TokenType.TYPE
      case _ if word in c_keywords:
        token_type = TokenType.KEYWORD
      case _ if word in c_functions:
        token_type = TokenType.FUNCTION
      case _:
        token_type = TokenType.IDENT
      
    return Token(token_type, word, start_index, reader.current_index)
  
  def handle_symbols(self, reader:Reader):
    start_index = reader.current_index
    
    symbol = reader.content[start_index]
    reader.advance()
    
    return Token(TokenType.PUNCTUATORS, symbol, start_index, reader.current_index )
  
  def handle_numbers(self, reader: Reader):
    start_index = reader.current_index
    
    while not reader.at_end() and reader.peek().isdigit():
      reader.advance()
    
    number = reader.content[start_index: reader.current_index]
    
    return Token(TokenType.NUMBER, number, start_index, reader.current_index)
  
def read_file_content(filepath:str) -> str:
  with open(filepath, "r") as file:
    return file.read()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="C Syntax Highlighter")
  parser.add_argument("filepath")
  args = parser.parse_args()
  filepath = args.filepath
  
  if not os.path.exists(filepath):
    print("Filepath provided does not exists...")
    sys.exit(1)
    
  lexer = Lexer()
  
  content = read_file_content(filepath=filepath)
  tokens = lexer.parse_code(content=content)
  
  print(len(tokens))
  for token in tokens:
    print(token)