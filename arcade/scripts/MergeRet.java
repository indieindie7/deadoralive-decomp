// MergeRet.java <addr>...: remove the stub function DOA_ret_<addr> and re-fix the function that falls into it
import ghidra.app.script.GhidraScript;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
public class MergeRet extends GhidraScript {
	@Override public void run() throws Exception {
		for (String s : getScriptArgs()) {
			Address a=toAddr(Long.parseLong(s,16));
			Function f=getFunctionAt(a);
			if(f!=null && f.getName().startsWith("DOA_ret_")) removeFunction(f);
			Instruction i=getInstructionAt(a); Instruction p=i==null?null:i.getPrevious();
			Function pf=p==null?null:getFunctionContaining(p.getAddress());
			if(pf!=null){ CreateFunctionCmd.fixupFunctionBody(currentProgram,pf,monitor); println("merged "+s+" into "+pf.getName()+" ret in body="+pf.getBody().contains(a)); }
			else println("no prev fn for "+s);
		}
	}
}
