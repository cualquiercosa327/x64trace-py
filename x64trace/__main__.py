
import x64trace
import sys

if len(sys.argv) != 2:
	print(f"usage: {sys.argv[0]} [trace file]")
	exit(1)

with open(sys.argv[1], "rb") as f:
	t = x64trace.Trace.load32(f)

try:
	import capstone
	cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
except ImportError:
	cs = None
	print("NOTE: Install capstone to get disassembly!")

for i, block in enumerate(t.blocks):
	ip = block.registers.regcontext.cip
	if cs is not None:
		for inst in cs.disasm(block.opcode, ip):
			print(f"{inst.address:#08x} {block.opcode.hex():32} {inst.mnemonic} {inst.op_str}")
	else:
		print(f"{ip:#08x} {block.opcode.hex()}")

