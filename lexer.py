import argparse
import os
import sys
from dataclasses import dataclass
from token_types import TokenType
from themes import AVAILABLE_THEMES, MONOKAI_THEME

parser = argparse.ArgumentParser(prog="C Syntax Highlighter")
parser.add_argument("filepath")
parser.add_argument("-theme", choices=AVAILABLE_THEMES, default=AVAILABLE_THEMES["MONOKAI_THEME"])

@dataclass(frozen=True, slots=True)
class Token():
  token_type: TokenType
  token_value: str
  token_color: str
  starting_pos: int
  ending_pos: int
  
type TokenList = list[Token]

def add_token_to_list(token_list: TokenList, new_token: Token):
  token_list.append(new_token)
  
def reset_variables(initial_index: int, current_index: int):
  return initial_index + 1, current_index + 1, ""

c_types = {"int", "float", "char"}
c_identifiers = {"main"} # this should not be a set. Identifiers are created during parsing, a user can identify a function by one name, while other user can identify it by another
c_punctuators = {'{','}', '(', ')', '[', ']', ';'}
c_keywords = {'return'}
c_functions = {'printf'}

def parse_code(content: str) -> TokenList:
  tokens: TokenList = []
  
  current_token: str = ""
  content_length = len(content)
  
  initial_index = 0
  current_index = 0
  
  is_in_string_literal = False
  
  while current_index < content_length:
    current_character = content[current_index]
    current_token += current_character
    
    if current_character.isspace():
      if not is_in_string_literal:
        current_token = ""
        
      current_index += 1
      continue
    
    # indentified number
    if current_character.isdigit():
      if current_index + 1 < content_length and not content[current_index + 1].isspace() and content[current_index + 1].isdigit():
        current_index += 1
        continue
      
      add_token_to_list(token_list=tokens, new_token=Token(TokenType.NUMBER, current_token, MONOKAI_THEME[TokenType.NUMBER], initial_index, current_index))
      initial_index, current_index, current_token = reset_variables(initial_index, current_index)
      continue
    
    if current_character == '"':
      if not is_in_string_literal:
        is_in_string_literal = True
        current_index += 1
        continue
      
      is_in_string_literal = False
      add_token_to_list(token_list=tokens, new_token=Token(TokenType.STRING_LITERAL, current_token, MONOKAI_THEME[TokenType.NUMBER], initial_index, current_index))
      initial_index, current_index, current_token = reset_variables(initial_index, current_index)
      continue
      
    match current_token:
      case _ if current_token in c_types:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.TYPE, current_token, MONOKAI_THEME[TokenType.TYPE], initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index)
        continue
      case _ if current_token in c_identifiers:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.IDENT, current_token, MONOKAI_THEME[TokenType.IDENT],initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index)
        continue
      case _ if current_token in c_punctuators:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.PUNCTUATORS, current_token, MONOKAI_THEME[TokenType.PUNCTUATORS], initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index)
        continue
      case _ if current_token in c_keywords:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.KEYWORD, current_token, MONOKAI_THEME[TokenType.OP], initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index)
        continue
      case _ if current_token in c_functions:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.FUNCTION, current_token, MONOKAI_THEME[TokenType.OP], initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index)
        continue
      case _:
        current_index += 1
        continue
        
    current_index += 1
    
  return tokens

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
  
  content = read_file_content(filepath=filepath)
  tokens = parse_code(content=content)
  
  print("Total tokens:", len(tokens))
  for token in tokens:
      print(token)