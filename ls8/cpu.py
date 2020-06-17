"""CPU functionality."""

import sys

LDI = 0b10000010
PRA = 0b01001000
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
DIV = 0b10100011
ADD = 0b10100000
SUB = 0b10100001
opcodes = [
    LDI,
    PRA,
    PRN,
    HLT,
    MUL,
    DIV,
    ADD,
    SUB,
]

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0
        self.branch_table = {
            LDI: self.handle_LDI,
            PRA: self.handle_PRA,
            PRN: self.handle_PRN,
            HLT: self.handle_HLT,
            MUL: self.handle_MUL,
            DIV: self.handle_DIV,
            ADD: self.handle_ADD,
            SUB: self.handle_SUB
        }

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            address = 0
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]
            for instruction in program:
                self.ram[address] = instruction
                address += 1
        # If there is 1 argument: load the program
        elif len(sys.argv) == 2:
            filename = sys.argv[1]
            with open(filename) as f:
                address = 0
                for line in f:
                    if line[0] != "#" or line[0] != " ":
                        line = line.split("#")
                        try:
                            v = int(line[0], 2)
                        except ValueError:
                            continue
                        self.ram[address] = v
                        address += 1
        else:
            print("You can only load one ls8 program. Usage: 'python ls8.py example.ls8'")
            sys.exit(1)
   
   
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True

        while running:
            value = self.ram[self.pc]
            self.ir = value

            # LDI: loads valueB into register at valueA...register[valueA] = valueB
            if self.ir == 0b10000010:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)
                self.register[operand_a] = operand_b
                self.pc += 3

            # PRA: prints alpha-character
            elif self.ir == 0b01001000:
                print(self.register[self.pc+1])
                self.pc += 2

            # PRN: prints a number
            elif self.ir == 0b01000111:
                index = self.ram_read(self.pc+1)
                print(self.register[index])
                self.pc += 2

            # HLT: ends run()
            elif self.ir == 0b00000001:
                running = False
        
        # running = None

        # while running == None:
        #     value = self.ram[self.pc]
    
        # if value not in opcodes:
        #     print(f"Unknown instruction {self.ir} at address {self.pc}")
        #     print(self.ram)
        #     running = False
        #     sys.exit(1)
        
        # else:
        #     self.ir = value
        #     running = self.branch_table[self.ir]()
        
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

