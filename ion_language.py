"""
ION Language Implementation
Intent-Deterministic Development Platform
Based on ION Research & Code Compendium (August 2026)

Developer: ADITYA KAMBLE
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class TokenType(Enum):
    """ION Token Types"""
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    OPERATOR = "OPERATOR"
    PUNCTUATION = "PUNCTUATION"
    INTENT = "INTENT"
    CONSTRAINT = "CONSTRAINT"
    EOF = "EOF"
    # Advanced type system tokens
    TYPE = "TYPE"
    GENERIC = "GENERIC"
    TRAIT = "TRAIT"
    IMPL = "IMPL"
    STRUCT = "STRUCT"
    ENUM = "ENUM"
    FN = "FN"
    LET = "LET"
    MUT = "MUT"
    CONST = "CONST"
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    MATCH = "MATCH"
    CASE = "CASE"
    FOR = "FOR"
    WHILE = "WHILE"
    TRY = "TRY"
    CATCH = "CATCH"
    FINALLY = "FINALLY"
    REALTIME = "REALTIME"
    CAPABILITY = "CAPABILITY"
    REQUIRES = "REQUIRES"
    ENSURES = "ENSURES"
    VERIFIED = "VERIFIED"
    MODEL_CHECK = "MODEL_CHECK"


@dataclass
class Token:
    """ION Token"""
    type: TokenType
    value: str
    line: int
    column: int


class IONLexer:
    """ION Language Lexer"""
    
    KEYWORDS = {'fn', 'struct', 'intent', 'return', 'if', 'else', 'true', 'false',
                'error', 'ok', 'constraint', 'when', 'on', 'verify', 'execute', 'invariant',
                # Advanced type system
                'let', 'mut', 'const', 'trait', 'impl', 'enum', 'match', 'case',
                'for', 'while', 'try', 'catch', 'finally', 'realtime',
                # Domain modules
                'robotics', 'quantum', 'ai', 'space', 'iot', 'bio', 'xr',
                # Security and verification
                'capability', 'requires', 'ensures', 'verified', 'model_check'}
    
    OPERATORS = {'=', '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', '->', ':', '.'}
    
    PUNCTUATION = {'(', ')', '{', '}', '[', ']', ',', ';'}
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self) -> List[Token]:
        """Tokenize ION source code"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
                
            char = self.source[self.pos]
            
            # Skip comments
            if char == '#':
                self.skip_comment()
                continue
            
            # String literals
            if char == '"':
                self.tokenize_string()
                continue
            
            # Numbers
            if char.isdigit() or (char == '-' and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
                self.tokenize_number()
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokenize_identifier()
                continue
            
            # Operators
            if char in self.OPERATORS:
                self.tokenize_operator()
                continue
            
            # Punctuation
            if char in self.PUNCTUATION:
                self.tokens.append(Token(TokenType.PUNCTUATION, char, self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            
            raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_comment(self):
        """Skip single-line comments"""
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1
    
    def tokenize_string(self):
        """Tokenize string literals"""
        start_pos = self.pos
        start_column = self.column
        self.pos += 1  # Skip opening quote
        self.column += 1
        
        value = ""
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            value += self.source[self.pos]
            self.pos += 1
            self.column += 1
        
        if self.pos >= len(self.source):
            raise SyntaxError("Unterminated string literal")
        
        self.pos += 1  # Skip closing quote
        self.column += 1
        self.tokens.append(Token(TokenType.STRING, value, self.line, start_column))
    
    def tokenize_number(self):
        """Tokenize number literals"""
        start_column = self.column
        start_pos = self.pos
        
        if self.source[self.pos] == '-':
            self.pos += 1
            self.column += 1
        
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
            self.column += 1
        
        # Decimal part
        if self.pos < len(self.source) and self.source[self.pos] == '.':
            self.pos += 1
            self.column += 1
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self.pos += 1
                self.column += 1
        
        value = self.source[start_pos:self.pos]
        self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_column))
    
    def tokenize_identifier(self):
        """Tokenize identifiers and keywords"""
        start_column = self.column
        start_pos = self.pos
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.pos += 1
            self.column += 1
        
        value = self.source[start_pos:self.pos]
        
        if value in self.KEYWORDS:
            self.tokens.append(Token(TokenType.KEYWORD, value, self.line, start_column))
        elif value == 'true' or value == 'false':
            self.tokens.append(Token(TokenType.BOOLEAN, value, self.line, start_column))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_column))
    
    def tokenize_operator(self):
        """Tokenize operators (including multi-character operators)"""
        start_column = self.column
        start_pos = self.pos
        
        # Check for multi-character operators first
        if self.pos + 1 < len(self.source):
            two_char = self.source[self.pos:self.pos + 2]
            if two_char in {'==', '!=', '<=', '>=', '->'}:
                self.tokens.append(Token(TokenType.OPERATOR, two_char, self.line, start_column))
                self.pos += 2
                self.column += 2
                return
        
        # Single character operator
        char = self.source[self.pos]
        self.tokens.append(Token(TokenType.OPERATOR, char, self.line, start_column))
        self.pos += 1
        self.column += 1


# AST Node Types
@dataclass
class ASTNode:
    """Base AST Node"""
    pass


@dataclass
class Program(ASTNode):
    """ION Program - root of AST"""
    statements: List[ASTNode]


@dataclass
class FunctionDecl(ASTNode):
    """Function Declaration"""
    name: str
    params: List[str]
    body: List[ASTNode]
    return_type: Optional[str] = None


@dataclass
class StructDecl(ASTNode):
    """Struct Declaration"""
    name: str
    fields: Dict[str, str]
    defaults: Dict[str, Any]


@dataclass
class IntentDecl(ASTNode):
    """Intent Declaration - ION's core innovation"""
    name: str
    endpoints: List[Dict[str, str]]
    constraints: List[Dict[str, str]]
    invariants: List[str]
    handlers: List[ASTNode]


@dataclass
class VariableDecl(ASTNode):
    """Variable Declaration"""
    name: str
    value: ASTNode
    var_type: Optional[str] = None


@dataclass
class BinaryOp(ASTNode):
    """Binary Operation"""
    operator: str
    left: ASTNode
    right: ASTNode


@dataclass
class FunctionCall(ASTNode):
    """Function Call"""
    name: str
    args: List[ASTNode]


@dataclass
class ReturnStmt(ASTNode):
    """Return Statement"""
    value: ASTNode


@dataclass
class IfStmt(ASTNode):
    """If Statement"""
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: List[ASTNode]


@dataclass
class ErrorResult(ASTNode):
    """Error Result"""
    message: ASTNode


@dataclass
class OkResult(ASTNode):
    """Ok Result"""
    value: ASTNode


@dataclass
class Literal(ASTNode):
    """Literal Value"""
    value: Union[str, int, float, bool]
    literal_type: Optional[str] = None  # For typed literals


@dataclass
class TypeAnnotation(ASTNode):
    """Type annotation for variables and functions"""
    type_name: str
    generic_params: List[str] = field(default_factory=list)
    is_mutable: bool = False
    is_optional: bool = False


@dataclass
class VariableDeclAdvanced(ASTNode):
    """Advanced variable declaration with type annotations"""
    name: str
    var_type: Optional[TypeAnnotation] = None
    value: Optional[ASTNode] = None
    is_mutable: bool = False
    is_const: bool = False


@dataclass
class TraitDecl(ASTNode):
    """Trait declaration (interface)"""
    name: str
    methods: List[FunctionDecl]
    generic_params: List[str] = field(default_factory=list)


@dataclass
class ImplBlock(ASTNode):
    """Implementation block for traits"""
    trait_name: Optional[str] = None  # None for inherent impl
    type_name: str = ""
    methods: List[FunctionDecl] = field(default_factory=list)


@dataclass
class EnumDecl(ASTNode):
    """Enum declaration"""
    name: str
    variants: List[Dict[str, Any]]
    generic_params: List[str] = field(default_factory=list)


@dataclass
class MatchExpr(ASTNode):
    """Match expression (pattern matching)"""
    value: ASTNode
    cases: List[Dict[str, Any]]  # Each case has pattern, guard, body


@dataclass
class ForLoop(ASTNode):
    """For loop with range and where clause"""
    variable: str
    range_expr: ASTNode
    where_clause: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class TryCatchBlock(ASTNode):
    """Try-catch-finally block"""
    try_body: List[ASTNode]
    catch_cases: List[Dict[str, Any]]  # exception type, variable name, body
    finally_body: List[ASTNode] = field(default_factory=list)


@dataclass
class RealtimeTask(ASTNode):
    """Real-time task declaration"""
    name: str
    period: ASTNode
    body: List[ASTNode]
    priority: int = 0


@dataclass
class CapabilityDecl(ASTNode):
    """Capability declaration for security"""
    name: str
    methods: List[FunctionDecl]
    permissions: List[str] = field(default_factory=list)


@dataclass
class CapabilitySpec(ASTNode):
    """Capability specification for functions"""
    capabilities: List[str]
    restrictions: List[str] = field(default_factory=list)


@dataclass
class VerificationSpec(ASTNode):
    """Formal verification specification"""
    requires: List[str] = field(default_factory=list)
    ensures: List[str] = field(default_factory=list)
    is_verified: bool = False
    is_model_checked: bool = False


@dataclass
class DomainImport(ASTNode):
    """Domain-specific module import"""
    domain: str  # robotics, quantum, ai, space, iot, bio, xr
    modules: List[str]
    aliases: Dict[str, str] = field(default_factory=dict)


class IONParser:
    """ION Language Parser"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def parse(self) -> Program:
        """Parse ION source code into AST"""
        statements = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    def advance(self):
        """Move to next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a statement"""
        if not self.current_token:
            return None

        # Function declaration
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'fn':
            return self.parse_function()

        # Struct declaration
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'struct':
            return self.parse_struct()

        # Intent declaration
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'intent':
            return self.parse_intent()

        # Trait declaration
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'trait':
            return self.parse_trait()

        # Enum declaration
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'enum':
            return self.parse_enum()

        # Implementation block
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'impl':
            return self.parse_impl()

        # Variable declarations (let, mut, const)
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value in ['let', 'mut', 'const']:
            return self.parse_variable_advanced()

        # Variable declaration (legacy)
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_variable()

        # Return statement
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'return':
            return self.parse_return()

        # If statement
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'if':
            return self.parse_if()

        # Match expression
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'match':
            return self.parse_match()

        # For loop
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'for':
            return self.parse_for_loop()

        # While loop
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'while':
            return self.parse_while_loop()

        # Try-catch block
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'try':
            return self.parse_try_catch()

        # Real-time task
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'realtime':
            return self.parse_realtime_task()

        # Capability declaration
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'capability':
            return self.parse_capability()

        # Domain import
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value in ['robotics', 'quantum', 'ai', 'space', 'iot', 'bio', 'xr']:
            return self.parse_domain_import()

        # Expression
        return self.parse_expression()
    
    def parse_function(self) -> FunctionDecl:
        """Parse function declaration"""
        self.advance()  # 'fn'
        name = self.current_token.value
        self.advance()
        
        # Parameters
        params = []
        if self.current_token.type == TokenType.PUNCTUATION and self.current_token.value == '(':
            self.advance()
            while self.current_token and self.current_token.value != ')':
                if self.current_token.type == TokenType.IDENTIFIER:
                    params.append(self.current_token.value)
                    self.advance()
                if self.current_token and self.current_token.value == ',':
                    self.advance()
            if self.current_token:
                self.advance()  # ')'
        
        # Body
        body = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            if self.current_token:
                self.advance()  # '}'
        
        return FunctionDecl(name, params, body)
    
    def parse_struct(self) -> StructDecl:
        """Parse struct declaration"""
        self.advance()  # 'struct'
        name = self.current_token.value
        self.advance()
        
        fields = {}
        defaults = {}
        
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                if self.current_token.type == TokenType.IDENTIFIER:
                    field_name = self.current_token.value
                    self.advance()
                    
                    if self.current_token and self.current_token.value == ':':
                        self.advance()
                        field_type = self.current_token.value
                        self.advance()
                        fields[field_name] = field_type
                        
                        # Default value
                        if self.current_token and self.current_token.value == '=':
                            self.advance()
                            default_val = self.parse_expression()
                            defaults[field_name] = default_val
                    
                    if self.current_token and self.current_token.value == ',':
                        self.advance()
            if self.current_token:
                self.advance()  # '}'
        
        return StructDecl(name, fields, defaults)
    
    def parse_intent(self) -> IntentDecl:
        """Parse intent declaration - ION's core feature"""
        self.advance()  # 'intent'
        name = self.current_token.value
        self.advance()
        
        endpoints = []
        constraints = []
        invariants = []
        handlers = []
        
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                # Endpoint definitions
                if self.current_token.type == TokenType.IDENTIFIER:
                    method = self.current_token.value
                    self.advance()
                    
                    if self.current_token and self.current_token.value == '/':
                        path = ""
                        self.advance()
                        while self.current_token and self.current_token.value != ' ' and self.current_token.value != '-':
                            path += self.current_token.value
                            self.advance()
                        
                        if self.current_token and self.current_token.value == '-':
                            self.advance()
                            if self.current_token and self.current_token.value == '>':
                                self.advance()
                                func_name = self.current_token.value
                                endpoints.append({'method': method, 'path': '/' + path, 'function': func_name})
                                self.advance()
                
                # Constraint definitions
                elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'constraint':
                    self.advance()
                    constraint_name = self.current_token.value
                    self.advance()
                    if self.current_token and self.current_token.value == ':':
                        self.advance()
                        constraint_value = self.current_token.value
                        constraints.append({'name': constraint_name, 'value': constraint_value})
                        self.advance()
                
                # Invariant definitions
                elif self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'invariant':
                    self.advance()
                    invariant_text = ""
                    while self.current_token and self.current_token.value != ',' and self.current_token.value != '}':
                        invariant_text += self.current_token.value + " "
                        self.advance()
                    invariants.append(invariant_text.strip())
                
                # Handler definitions (when, on, verify, execute)
                elif self.current_token.type == TokenType.KEYWORD and self.current_token.value in ['when', 'on', 'verify', 'execute']:
                    handler = self.parse_handler()
                    if handler:
                        handlers.append(handler)
                
                # Skip commas and other separators
                if self.current_token and self.current_token.value == ',':
                    self.advance()
            
            if self.current_token:
                self.advance()  # '}'
        
        return IntentDecl(name, endpoints, constraints, invariants, handlers)
    
    def parse_handler(self) -> Optional[ASTNode]:
        """Parse intent handler (when, on, verify, execute)"""
        handler_type = self.current_token.value
        self.advance()

        # Simple handler structure for prototype
        condition = self.parse_expression()

        body = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            if self.current_token:
                self.advance()

        # Return a generic function call as placeholder
        return FunctionCall(handler_type, [condition])

    def parse_trait(self) -> TraitDecl:
        """Parse trait declaration"""
        self.advance()  # 'trait'
        name = self.current_token.value
        self.advance()

        methods = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'fn':
                    method = self.parse_function()
                    methods.append(method)
                if self.current_token and self.current_token.value == ',':
                    self.advance()
            if self.current_token:
                self.advance()  # '}'

        return TraitDecl(name=name, methods=methods)

    def parse_enum(self) -> EnumDecl:
        """Parse enum declaration"""
        self.advance()  # 'enum'
        name = self.current_token.value
        self.advance()

        variants = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                if self.current_token.type == TokenType.IDENTIFIER:
                    variant_name = self.current_token.value
                    self.advance()

                    variant_data = {'name': variant_name, 'fields': []}

                    # Check for variant with data
                    if self.current_token and self.current_token.value == '(':
                        self.advance()
                        while self.current_token and self.current_token.value != ')':
                            if self.current_token.type == TokenType.IDENTIFIER:
                                variant_data['fields'].append(self.current_token.value)
                                self.advance()
                            if self.current_token and self.current_token.value == ',':
                                self.advance()
                        if self.current_token:
                            self.advance()  # ')'

                    variants.append(variant_data)

                if self.current_token and self.current_token.value == ',':
                    self.advance()
                elif self.current_token and self.current_token.value == '|':
                    self.advance()

            if self.current_token:
                self.advance()  # '}'

        return EnumDecl(name=name, variants=variants)

    def parse_impl(self) -> ImplBlock:
        """Parse implementation block"""
        self.advance()  # 'impl'

        trait_name = None
        type_name = ""

        # Check if it's a trait implementation
        if self.current_token.type == TokenType.IDENTIFIER:
            potential_trait = self.current_token.value
            self.advance()
            if self.current_token and self.current_token.value == 'for':
                trait_name = potential_trait
                self.advance()
                type_name = self.current_token.value
                self.advance()
            else:
                # Inherent implementation
                type_name = potential_trait

        methods = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'fn':
                    method = self.parse_function()
                    methods.append(method)
                if self.current_token and self.current_token.value == ',':
                    self.advance()
            if self.current_token:
                self.advance()  # '}'

        return ImplBlock(trait_name=trait_name, type_name=type_name, methods=methods)

    def parse_variable_advanced(self) -> VariableDeclAdvanced:
        """Parse advanced variable declaration (let, mut, const)"""
        keyword = self.current_token.value
        self.advance()

        is_mutable = keyword == 'mut'
        is_const = keyword == 'const'

        name = self.current_token.value
        self.advance()

        # Type annotation
        var_type = None
        if self.current_token and self.current_token.value == ':':
            self.advance()
            var_type = self.parse_type_annotation()

        # Value
        value = None
        if self.current_token and self.current_token.value == '=':
            self.advance()
            value = self.parse_expression()

        return VariableDeclAdvanced(
            name=name,
            var_type=var_type,
            value=value,
            is_mutable=is_mutable,
            is_const=is_const
        )

    def parse_type_annotation(self) -> TypeAnnotation:
        """Parse type annotation"""
        type_name = self.current_token.value
        self.advance()

        generic_params = []
        if self.current_token and self.current_token.value == '<':
            self.advance()
            while self.current_token and self.current_token.value != '>':
                if self.current_token.type == TokenType.IDENTIFIER:
                    generic_params.append(self.current_token.value)
                    self.advance()
                if self.current_token and self.current_token.value == ',':
                    self.advance()
            if self.current_token:
                self.advance()  # '>'

        return TypeAnnotation(type_name=type_name, generic_params=generic_params)

    def parse_match(self) -> MatchExpr:
        """Parse match expression"""
        self.advance()  # 'match'
        value = self.parse_expression()

        cases = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'case':
                    self.advance()
                    pattern = self.parse_expression()

                    # Optional guard
                    guard = None
                    if self.current_token and self.current_token.value == 'if':
                        self.advance()
                        guard = self.parse_expression()

                    # Body
                    body = []
                    if self.current_token and self.current_token.value == ':':
                        self.advance()
                        while self.current_token and self.current_token.value not in ['case', '}']:
                            stmt = self.parse_statement()
                            if stmt:
                                body.append(stmt)

                    cases.append({'pattern': pattern, 'guard': guard, 'body': body})

            if self.current_token:
                self.advance()  # '}'

        return MatchExpr(value=value, cases=cases)

    def parse_for_loop(self) -> ForLoop:
        """Parse for loop"""
        self.advance()  # 'for'
        variable = self.current_token.value
        self.advance()

        if self.current_token and self.current_token.value == 'in':
            self.advance()
            range_expr = self.parse_expression()

            # Optional where clause
            where_clause = None
            if self.current_token and self.current_token.value == 'where':
                self.advance()
                where_clause = self.parse_expression()

            body = []
            if self.current_token and self.current_token.value == ':':
                self.advance()
                while self.current_token and self.current_token.value != '}':
                    stmt = self.parse_statement()
                    if stmt:
                        body.append(stmt)
                if self.current_token:
                    self.advance()

            return ForLoop(variable=variable, range_expr=range_expr, where_clause=where_clause, body=body)

        return ForLoop(variable=variable, range_expr=Literal(0), body=[])

    def parse_while_loop(self) -> ForLoop:
        """Parse while loop (simplified as for loop for prototype)"""
        self.advance()  # 'while'
        condition = self.parse_expression()

        body = []
        if self.current_token and self.current_token.value == ':':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            if self.current_token:
                self.advance()

        # Represent as for loop for prototype
        return ForLoop(variable="_while_", range_expr=condition, body=body)

    def parse_try_catch(self) -> TryCatchBlock:
        """Parse try-catch-finally block"""
        self.advance()  # 'try'

        try_body = []
        if self.current_token and self.current_token.value == ':':
            self.advance()
            while self.current_token and self.current_token.value not in ['catch', 'finally']:
                stmt = self.parse_statement()
                if stmt:
                    try_body.append(stmt)

        catch_cases = []
        if self.current_token and self.current_token.value == 'catch':
            while self.current_token and self.current_token.value == 'catch':
                self.advance()
                exception_type = self.current_token.value
                self.advance()

                exception_var = None
                if self.current_token and self.current_token.value == 'as':
                    self.advance()
                    exception_var = self.current_token.value
                    self.advance()

                catch_body = []
                if self.current_token and self.current_token.value == ':':
                    self.advance()
                    while self.current_token and self.current_token.value not in ['catch', 'finally']:
                        stmt = self.parse_statement()
                        if stmt:
                            catch_body.append(stmt)

                catch_cases.append({
                    'exception_type': exception_type,
                    'variable': exception_var,
                    'body': catch_body
                })

        finally_body = []
        if self.current_token and self.current_token.value == 'finally':
            self.advance()
            if self.current_token and self.current_token.value == ':':
                self.advance()
                while self.current_token and self.current_token.value != '}':
                    stmt = self.parse_statement()
                    if stmt:
                        finally_body.append(stmt)

        return TryCatchBlock(try_body=try_body, catch_cases=catch_cases, finally_body=finally_body)

    def parse_realtime_task(self) -> RealtimeTask:
        """Parse real-time task declaration"""
        self.advance()  # 'realtime'
        self.advance()  # 'task'

        name = self.current_token.value
        self.advance()

        # Period
        period = None
        if self.current_token and self.current_token.value == '(':
            self.advance()
            period = self.parse_expression()
            if self.current_token and self.current_token.value == ')':
                self.advance()

        body = []
        if self.current_token and self.current_token.value == ':':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            if self.current_token:
                self.advance()

        return RealtimeTask(name=name, period=period, body=body)

    def parse_capability(self) -> CapabilityDecl:
        """Parse capability declaration"""
        self.advance()  # 'capability'
        name = self.current_token.value
        self.advance()

        methods = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'fn':
                    method = self.parse_function()
                    methods.append(method)
                if self.current_token and self.current_token.value == ',':
                    self.advance()
            if self.current_token:
                self.advance()  # '}'

        return CapabilityDecl(name=name, methods=methods)

    def parse_domain_import(self) -> DomainImport:
        """Parse domain-specific module import"""
        domain = self.current_token.value
        self.advance()

        modules = []
        if self.current_token and self.current_token.value == '::':
            self.advance()
            while self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                modules.append(self.current_token.value)
                self.advance()
                if self.current_token and self.current_token.value == ',':
                    self.advance()

        return DomainImport(domain=domain, modules=modules)
    
    def parse_variable(self) -> VariableDecl:
        """Parse variable declaration"""
        name = self.current_token.value
        self.advance()
        
        if self.current_token and self.current_token.value == '=':
            self.advance()
            value = self.parse_expression()
            return VariableDecl(name, value)
        
        return VariableDecl(name, Literal(None))
    
    def parse_return(self) -> ReturnStmt:
        """Parse return statement"""
        self.advance()  # 'return'
        value = self.parse_expression()
        return ReturnStmt(value)
    
    def parse_if(self) -> IfStmt:
        """Parse if statement"""
        self.advance()  # 'if'
        condition = self.parse_expression()
        
        then_body = []
        if self.current_token and self.current_token.value == '{':
            self.advance()
            while self.current_token and self.current_token.value != '}':
                stmt = self.parse_statement()
                if stmt:
                    then_body.append(stmt)
            if self.current_token:
                self.advance()
        
        else_body = []
        if self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'else':
            self.advance()
            if self.current_token and self.current_token.value == '{':
                self.advance()
                while self.current_token and self.current_token.value != '}':
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)
                if self.current_token:
                    self.advance()
        
        return IfStmt(condition, then_body, else_body)
    
    def parse_expression(self) -> ASTNode:
        """Parse expression"""
        return self.parse_binary_op()
    
    def parse_binary_op(self) -> ASTNode:
        """Parse binary operations with precedence"""
        left = self.parse_primary()
        
        while self.current_token and self.current_token.type == TokenType.OPERATOR:
            operator = self.current_token.value
            self.advance()
            right = self.parse_primary()
            left = BinaryOp(operator, left, right)
        
        return left
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions"""
        if not self.current_token:
            return Literal(None)
        
        # Parenthesized expression
        if self.current_token.type == TokenType.PUNCTUATION and self.current_token.value == '(':
            self.advance()
            expr = self.parse_expression()
            if self.current_token and self.current_token.value == ')':
                self.advance()
            return expr
        
        # String literal
        if self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()
            return Literal(value)
        
        # Number literal
        if self.current_token.type == TokenType.NUMBER:
            value_str = self.current_token.value
            self.advance()
            if '.' in value_str:
                return Literal(float(value_str))
            return Literal(int(value_str))
        
        # Boolean literal
        if self.current_token.type == TokenType.BOOLEAN:
            value = self.current_token.value == 'true'
            self.advance()
            return Literal(value)
        
        # Identifier
        if self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
            
            # Function call
            if self.current_token and self.current_token.value == '(':
                self.advance()
                args = []
                while self.current_token and self.current_token.value != ')':
                    arg = self.parse_expression()
                    if arg:
                        args.append(arg)
                    if self.current_token and self.current_token.value == ',':
                        self.advance()
                if self.current_token:
                    self.advance()
                return FunctionCall(name, args)
            
            # Property access
            if self.current_token and self.current_token.value == '.':
                self.advance()
                property_name = self.current_token.value
                self.advance()
                return FunctionCall(f"{name}.{property_name}", [])
            
            return Literal(name)
        
        # Error/Ok results
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'error':
            self.advance()
            if self.current_token and self.current_token.value == '(':
                self.advance()
                message = self.parse_expression()
                if self.current_token and self.current_token.value == ')':
                    self.advance()
                return ErrorResult(message)
        
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'ok':
            self.advance()
            if self.current_token and self.current_token.value == '(':
                self.advance()
                value = self.parse_expression()
                if self.current_token and self.current_token.value == ')':
                    self.advance()
                return OkResult(value)
        
        return Literal(None)


def parse_ion(source: str) -> Program:
    """Parse ION source code"""
    lexer = IONLexer(source)
    tokens = lexer.tokenize()
    parser = IONParser(tokens)
    return parser.parse()


if __name__ == "__main__":
    # Test ION parsing
    ion_code = """
# ION Hello World
print("Hello, World!")

# Function with type inference
fn greet(name):
    return "Hello, " + name

# Struct declaration
struct User:
    name: string
    age: number
    active: bool = true

# Intent declaration
intent UserService:
    get /users -> list_all()
    post /users -> create_user(body)
    
    constraint auth: jwt
    constraint rate: 100/min
"""
    
    try:
        program = parse_ion(ion_code)
        print("ION Parser - Successfully parsed program")
        print(f"Number of statements: {len(program.statements)}")
    except Exception as e:
        print(f"Parse error: {e}")