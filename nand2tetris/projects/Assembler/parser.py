# Goal of the parser is to break each assembly command (A or C CPU-instruction)
# into its underlying components.
# Reads an assembly language command, parses it and provides convenient access 
# to the command's components (fields and symbols).
# Also, it detects and removes whitespaces and comments

import sys


class Parser:
    def __init__(self, source_file: str):
        self.source_file = source_file              # Loads the source file
        self.assembly_program = self.open_file()  
        self.assembly_program_len = self.get_program_length() 

    line_counter = 0

    
    def open_file(self):
        '''Method removes whitespaces and comments of the provided 
        assembler source file. Returns a string'''

        cleaned_assembler_program = ''

        try:
            with open(self.source_file, 'r') as f:
                for line in f:
                    if line.startswith('//'):
                        pass
                    else:
                        cleaned_assembler_program += line.strip() + '\n'

        except FileNotFoundError as error:
            print(error)
            sys.exit(0)

        return cleaned_assembler_program.strip()


    def remove_labels(self):
        '''Method removes (XXX) labels from the assembly program.
        Returns string'''

        self.assembly_program = self.assembly_program.splitlines()
        labels_removed = ''

        for index, line in enumerate(self.assembly_program):
            if line.startswith('('):
                del self.assembly_program[index]
                self.assembly_program_len -= 1

        for line in self.assembly_program:
            labels_removed += line + '\n'
            
        return labels_removed.strip()

    
    def get_program_length(self):
        return len(self.assembly_program.split('\n'))
                    
    
    def is_parsed(self):
        '''Method stores the number of lines of the assembly program.
        Returns True when the program is parsed, else advances to the next line'''

        return self.assembly_program_len == self.line_counter


    def advance(self):
        '''Method reads the next command from the assembly program and makes it
        the current command. Should only be called while self.is_parsed is False'''

        if self.line_counter >= self.assembly_program_len:
            self.is_parsed()

        # Select command
        current_command = self.assembly_program.splitlines()[self.line_counter]
        # Advance to next command
        self.line_counter += 1

        return current_command

    
    def command_type(self, command):
        '''Method returns the type of the current CPU command:
            A_COMMAND - for @xxx where xxx is either a symbol or a decimal number;
            C_COMMAND - for dest=comp;jump;
            L_COMMAND - pseudo-command for (XXX) where XXX is a symbol (label);'''
        
        if command.startswith('@'):
            return 'A_COMMAND'
        elif command.startswith('('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'


    def is_decimal(self, command):
        '''Method returns True when the current A_COMMAND is a decimal number,
        else returns False, when the command is a symbol.
        Should only be called if self.command_type() is A_COMMAND.'''

        try:
            int(command)
            return True
        except:
            return False
        

    def dest_mnemonics(self, command):
        '''Returns the dest mnemonic (string) in the current C-command (8 possibilities).
        Should be called only when command_type() is C_COMMAND'''

        if '=' in command:
            return command.split('=')[0]


    def comp_mnemonics(self, command):
        '''Returns the comp mnemonic (string) in the current C-command (28 possibilities).
        Should be called only when self.command_type() is C_COMMAND'''

        if ';' in command:
            return command.split(';')[0]
        else:
            return command.split('=')[1]


    def jump_mnemonics(self, command):
        '''Returns the jump mnemonic (string) in the current C-command (8 possibilities)
        Should be called only when self.command_type() is C_COMMAND'''

        if ';' in command:
            return command.split(';')[1]