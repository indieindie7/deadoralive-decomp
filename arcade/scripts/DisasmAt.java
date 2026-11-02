// DisasmAt.java <file of hex addrs>: disassemble at each and re-fix owner function body (or create function)
import ghidra.app.script.GhidraScript;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;
public class DisasmAt extends GhidraScript {
	@Override public void run() throws Exception {
		for (String l : Files.readAllLines(Paths.get(getScriptArgs()[0]))) {
			l=l.trim(); if(l.isEmpty()) continue;
			Address a=toAddr(Long.parseLong(l,16));
			boolean ok=disassemble(a);
			Function f=getFunctionContaining(a);
			if(f==null){ f=createFunction(a,"DOA_ret_"+l); println("new fn "+l+" "+(f!=null)); }
			else { CreateFunctionCmd.fixupFunctionBody(currentProgram,f,monitor); println("fixed "+f.getName()+" for "+l+" dis="+ok+" instr="+(getInstructionAt(a)!=null)); }
		}
	}
}
