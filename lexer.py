import argparse
import os
import sys
from dataclasses import dataclass
from token_types import TokenType
from themes import AVAILABLE_THEMES, MONOKAI_THEME
from state_machine import LexerStateMachine, LexerEvents, LexerStates, LexerDirective

parser = argparse.ArgumentParser(prog="C Syntax Highlighter")
parser.add_argument("filepath")
parser.add_argument("-theme", choices=AVAILABLE_THEMES, default=AVAILABLE_THEMES["MONOKAI_THEME"])

c_types = {"int", "float", "char"}
c_identifiers = {"main"} # this should not be a set. Identifiers are created during parsing, a user can identify a function by one name, while other user can identify it by another
c_punctuators = {'{','}', '(', ')', '[', ']', ';'}
c_keywords = {'return'}
c_functions = {'printf'}

@dataclass(frozen=True, slots=True)
class Token:
  token_type: TokenType
  token_value: str
  token_color: str
  starting_pos: int
  ending_pos: int
  
type TokenList = list[Token]

class Lexer:
  def __init__(self):
    self.token_list: TokenList = []
  
    self.current_token: str = ""
    
    self.initial_index = 0
    self.current_index = 0
    
    self.state_machine = LexerStateMachine()

  def add_token_to_list(self, new_token: Token):
    self.token_list.append(new_token)
    self.reset_variables()
  
  def reset_variables(self) -> None:
    self.initial_index = self.initial_index + 1
    self.current_index = self.current_index + 1
    self.current_token = ""
  
  def parse_code(self, content:str) -> TokenList:
    content_length = len(content)
    
    while self.current_index < content_length:
      current_character = content[self.current_index]
      self.current_token += current_character
      
      if current_character.isspace():
        if self.state_machine.state != LexerStates.STRING:
          self.current_token = ""
          
        self.current_index += 1
        continue
      
      # indentified number
      if current_character.isdigit():
        if self.current_index + 1 < content_length and not content[self.current_index + 1].isspace() and content[self.current_index + 1].isdigit():
          self.current_index += 1
          continue
        
        self.add_token_to_list(new_token=Token(TokenType.NUMBER, self.current_token, MONOKAI_THEME[TokenType.NUMBER], self.initial_index, self.current_index))
        continue

      # indentified string
      if current_character == '"':
        res = self.state_machine.on_event(LexerEvents.FOUND_QUOTATION_MARKS)
        if res == LexerDirective.CONTINUE:
          self.current_index += 1
          continue
        elif res == LexerDirective.SAVE_TOKEN:
          self.add_token_to_list(new_token=Token(TokenType.STRING_LITERAL, self.current_token, MONOKAI_THEME[TokenType.NUMBER], self.initial_index, self.current_index))
          continue

      match self.current_token:
        case _ if self.current_token in c_types:
          self.add_token_to_list(new_token=Token(TokenType.TYPE, self.current_token, MONOKAI_THEME[TokenType.TYPE], self.initial_index, self.current_index))
          continue
        case _ if self.current_token in c_identifiers:
          self.add_token_to_list(new_token=Token(TokenType.IDENT, self.current_token, MONOKAI_THEME[TokenType.IDENT], self.initial_index, self.current_index))
          continue
        case _ if self.current_token in c_punctuators:
          self.add_token_to_list(new_token=Token(TokenType.PUNCTUATORS, self.current_token, MONOKAI_THEME[TokenType.PUNCTUATORS], self.initial_index, self.current_index))
          continue
        case _ if self.current_token in c_keywords:
          self.add_token_to_list(new_token=Token(TokenType.KEYWORD, self.current_token, MONOKAI_THEME[TokenType.OP], self.initial_index, self.current_index))
          continue
        case _ if self.current_token in c_functions:
          self.add_token_to_list(new_token=Token(TokenType.FUNCTION, self.current_token, MONOKAI_THEME[TokenType.OP], self.initial_index, self.current_index))
          continue
        case _:
          self.current_index += 1
          continue
          
      self.current_index += 1
      
    return self.token_list
  

def read_file_content(filepath:str) -> str:
  with open(filepath, "r") as file:
    return file.read()

if __name__ == "__main__":
  args = parser.parse_args()
  filepath = args.filepath
  theme = args.theme
  
  if not os.path.exists(filepath):
    print("Filepath provided does not exists...")
    sys.exit(1)
    
  lexer = Lexer()
  
  content = read_file_content(filepath=filepath)
  tokens = lexer.parse_code(content=content)
  
  for token in tokens:
    print(token)