// ExportInstr.java <out.tsv>: one line per instruction: addr len owner-function-entry (or -)
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.io.*;

public class ExportInstr extends GhidraScript {
	@Override
	public void run() throws Exception {
		PrintWriter w = new PrintWriter(new FileWriter(getScriptArgs()[0]));
		int n = 0;
		for (Instruction i : currentProgram.getListing().getInstructions(true)) {
			Function f = getFunctionContaining(i.getAddress());
			w.println(Long.toHexString(i.getAddress().getOffset()) + "\t" + i.getLength() + "\t" + (f == null ? "-" : Long.toHexString(f.getEntryPoint().getOffset())));
			n++;
		}
		w.close();
		println("instr " + n);
	}
}
