import argparse
import os
import sys
from enum import Enum
from dataclasses import dataclass

parser = argparse.ArgumentParser(prog="C Syntax Highlighter")
parser.add_argument("filepath")

class TokenType(Enum):
  PREPOC = "prepoc", # #include, #define, #if, etc.
  KEYWORD = "keyword" # if, return, while, typedef,
  TYPE = "type" #int, char, float, void,
  IDENT = "ident" # names
  NUMBER = "number"
  STRING_LITERAL = "string_literal", # everything inside double quote ""
  CHAR = "char" # everything inside ''
  COMMENT = "commment" # everything followed by // or /* */
  OP = "operators" # + -
  WHITESPACE = "whitespace" # /n
  PUNCTUATORS = "punctuators" # ; ( ) [ ] { }
  UNKNOWN = "unknown" # unknown tokens
  
@dataclass(frozen=True, slots=True)
class Token():
  token_type: TokenType
  token_value: str
  starting_pos: int
  ending_pos: int
  
type TokenList = list[Token]

def add_token_to_list(token_list: TokenList, new_token: Token):
  token_list.append(new_token)
  
def reset_variables(initial_index: int, current_index: int, current_token:str):
  initial_index = current_index
  current_token = ""
  current_index += 1

def parse_code(content: str) -> TokenList:
  c_types = {"int", "float", "char"}
  c_identifiers = {"main"}
  c_punctuators = {'{','}', '(', ')', '[', ']', ';'}
  c_keywords = {'return'}
  
  tokens: TokenList = []
  
  current_token: str = ""
  content_length = len(content)
  
  initial_index = 0
  current_index = 0
  
  while current_index < content_length:
    c = content[current_index]
    current_token += c
    
    if c.isspace():
      if current_token[0] == '"':
        current_index += 1
        continue
      current_token = ""
      current_index += 1
      continue
    
    if len(current_token) == 1:
      # detect if this is a start of new word
      initial_index = current_index
    
    match current_token:
      case _ if current_token in c_types:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.TYPE, current_token, initial_index, current_index))
        reset_variables(initial_index, current_index, current_token)
        continue
      case _ if current_token in c_identifiers:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.IDENT, current_token, initial_index, current_index))
        reset_variables(initial_index, current_index, current_token)
        continue
      case _ if current_token in c_punctuators:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.PUNCTUATORS, current_token, initial_index, current_index))
        reset_variables(initial_index, current_index, current_token)
        continue
      case _ if current_token in c_keywords:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.OP, current_token, initial_index, current_index))
        reset_variables(initial_index, current_index, current_token)
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
  if not os.path.exists(filepath):
    print("Filepath provided does not exists...")
    sys.exit(1)
    
  content = read_file_content(filepath=filepath)
  tokens = parse_code(content=content)
  print(len(tokens), tokens)