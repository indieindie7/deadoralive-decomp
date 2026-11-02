// FixOwner.java <hex addr>...: re-fix the body of the function containing each address (follows branches that were missed).
import ghidra.app.script.GhidraScript;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.listing.*;

public class FixOwner extends GhidraScript {
	@Override
	public void run() throws Exception {
		for (String s : getScriptArgs()) {
			Function f = getFunctionContaining(toAddr(Long.parseLong(s, 16)));
			if (f == null) { println("no fn at " + s); continue; }
			CreateFunctionCmd.fixupFunctionBody(currentProgram, f, monitor);
			println("fixed " + f.getName() + " body " + f.getBody().getNumAddresses());
		}
	}
}
