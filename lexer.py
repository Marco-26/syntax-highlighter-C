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
  
MONOKAI_THEME = {
  TokenType.PREPOC: "#F92672",
  TokenType.KEYWORD: "#F92672",
  TokenType.TYPE: "#66D9EF",
  TokenType.IDENT: "#F8F8F2",
  TokenType.NUMBER: "#AE81FF",
  TokenType.STRING_LITERAL: "#E6DB74",
  TokenType.CHAR: "#E6DB74",
  TokenType.COMMENT: "#75715E",
  TokenType.OP: "#F92672",
  TokenType.WHITESPACE: "#F8F8F2",
  TokenType.PUNCTUATORS: "#F8F8F2",
  TokenType.UNKNOWN: "#FD971F",
}
  
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
  
def reset_variables(initial_index: int, current_index: int, current_token:str):
  initial_index = current_index
  current_token = ""
  current_index += 1
  return initial_index, current_index, current_token

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
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.TYPE, current_token, MONOKAI_THEME[TokenType.TYPE], initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index, current_token)
        continue
      case _ if current_token in c_identifiers:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.IDENT, current_token, MONOKAI_THEME[TokenType.IDENT],initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index, current_token)
        continue
      case _ if current_token in c_punctuators:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.PUNCTUATORS, current_token, MONOKAI_THEME[TokenType.PUNCTUATORS], initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index, current_token)
        continue
      case _ if current_token in c_keywords:
        add_token_to_list(token_list=tokens, new_token=Token(TokenType.OP, current_token, MONOKAI_THEME[TokenType.OP], initial_index, current_index))
        initial_index, current_index, current_token = reset_variables(initial_index, current_index, current_token)
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
  
  print("Total tokens:", len(tokens))
  for token in tokens:
      print(token)