// AddJumpTables.java <jtab.tsv>: lines "bx\ttable\tcount\tstatus\tt1,t2,..". Adds COMPUTED_JUMP refs bx->targets, disassembles targets, types the table as pointer dwords, re-fixes the owning function body.
import ghidra.app.script.GhidraScript;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.data.*;
import java.nio.file.*;
import java.util.*;

public class AddJumpTables extends GhidraScript {
	@Override
	public void run() throws Exception {
		int nt = 0, nr = 0, nf = 0, nnew = 0;
		Listing li = currentProgram.getListing();
		for (String l : Files.readAllLines(Paths.get(getScriptArgs()[0]))) {
			String[] p = l.trim().split("\t");
			if (p.length < 5) continue;
			Address bx = toAddr(Long.parseLong(p[0], 16));
			Address tab = toAddr(Long.parseLong(p[1], 16));
			int n = Integer.parseInt(p[2]);
			String[] ts = p[4].split(",");
			Function owner = getFunctionContaining(bx);
			for (int k = 0; k < ts.length; k++) {
				Address t = toAddr(Long.parseLong(ts[k], 16));
				currentProgram.getReferenceManager().addMemoryReference(bx, t, RefType.COMPUTED_JUMP, SourceType.USER_DEFINED, 0);
				nr++;
				if (li.getInstructionAt(t) == null) { disassemble(t); nnew++; }
				try {
					Address ea = tab.add(4L * k);
					li.clearCodeUnits(ea, ea.add(3), false);
					li.createData(ea, PointerDataType.dataType);
					currentProgram.getReferenceManager().addMemoryReference(ea, t, RefType.DATA, SourceType.USER_DEFINED, 0);
				} catch (Exception e) { }
			}
			nt++;
			if (owner != null) {
				try { CreateFunctionCmd.fixupFunctionBody(currentProgram, owner, monitor); nf++; } catch (Exception e) { println("fixup fail " + owner.getName() + " " + e); }
			}
		}
		println("tables " + nt + " refs " + nr + " newInstrStarts " + nnew + " fixups " + nf);
	}
}
