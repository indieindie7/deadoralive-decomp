import ghidra.app.script.GhidraScript;
public class ChkRet extends GhidraScript {
  public void run() throws Exception {
    for (String a : getScriptArgs()) {
      ghidra.program.model.address.Address ad = toAddr(Long.parseLong(a,16));
      ghidra.program.model.listing.Function f = getFunctionContaining(ad);
      println("RET " + a + " fn=" + (f==null?"NONE":f.getName()+"@"+f.getEntryPoint()) + " insn=" + getInstructionAt(ad) + " data=" + getDataAt(ad));
    }
  }
}
