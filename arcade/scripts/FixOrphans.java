// FixOrphans.java <real.txt> <junk.txt>: junk = orphan instruction addresses inside data (cleared); real = cluster starts that become functions (or extend the function they fall through from).
import ghidra.app.script.GhidraScript;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;

public class FixOrphans extends GhidraScript {
	@Override
	public void run() throws Exception {
		Listing li = currentProgram.getListing();
		int nj = 0, nf = 0, nx = 0;
		for (String l : Files.readAllLines(Paths.get(getScriptArgs()[1]))) {
			l = l.trim(); if (l.isEmpty()) continue;
			Address a = toAddr(Long.parseLong(l, 16));
			Instruction i = li.getInstructionAt(a);
			if (i != null && getFunctionContaining(a) == null) { li.clearCodeUnits(a, a.add(i.getLength() - 1), false); nj++; }
		}
		for (String l : Files.readAllLines(Paths.get(getScriptArgs()[0]))) {
			l = l.trim(); if (l.isEmpty()) continue;
			Address a = toAddr(Long.parseLong(l, 16));
			if (getFunctionContaining(a) != null) continue;
			Instruction i = li.getInstructionAt(a);
			Instruction p = i == null ? null : i.getPrevious();
			Function pf = p == null ? null : getFunctionContaining(p.getAddress());
			if (pf != null && p.isFallthrough() && p.getFallThrough() != null && p.getFallThrough().equals(a)) {
				CreateFunctionCmd.fixupFunctionBody(currentProgram, pf, monitor); nx++;
			} else {
				if (i == null) disassemble(a);
				createFunction(a, "DOA_orph_" + Long.toHexString(a.getOffset())); nf++;
			}
		}
		println("junk cleared " + nj + " funcs created " + nf + " extended " + nx);
	}
}
