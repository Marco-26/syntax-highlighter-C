# read in text file based on what is received in cli args.
# parse it to get the tokens
# based on token types assign a color

import argparse
import os
import sys
from enum import Enum

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
  OP = "operators" # ( ) + -
  WHITESPACE = "whitespace" # /n
  
class Token():
  token_type: TokenType
  token_value: str

def parse_code(content: str) -> list[tuple[TokenType, int, int]]:
  c_types = {"int", "float", "char"}
  c_identifiers = {"main"}
  tokens: list[tuple[TokenType, int, int]] = []
  
  current_token: str = ""
  content_length = len(content)
  
  initial_index = 0
  current_index = 0
  
  while current_index < content_length:
    c = content[current_index]
    current_token += c
    print(current_token, initial_index, current_index)
    
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
    
    if current_token in c_types:
      tokens.append((TokenType.TYPE, initial_index, current_index))
      initial_index = current_index
      current_token = ""
      current_index += 1
      continue
      
    if current_token in c_identifiers:
      tokens.append((TokenType.IDENT, initial_index, current_index))
      initial_index = current_index
      current_token = ""
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
  print(tokens)