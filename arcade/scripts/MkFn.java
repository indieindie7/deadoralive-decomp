import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
public class MkFn extends GhidraScript {
  public void run() throws Exception {
    String[] t = getScriptArgs();
    Address s = toAddr(Long.parseLong(t[0],16)), e = toAddr(Long.parseLong(t[1],16));
    Function old = getFunctionContaining(e);
    if (old != null && !old.getEntryPoint().equals(s)) { println("MKFN owner at end: " + old.getName() + " " + old.getBody()); }
    if (old != null && !old.getEntryPoint().equals(s)) { AddressSet ob = new AddressSet(old.getBody()); ob.delete(s, e); old.setBody(ob); }
    Function f = getFunctionAt(s);
    if (f == null) f = createFunction(s, t[2]);
    if (f == null) { println("MKFN FAIL"); return; }
    f.setName(t[2], ghidra.program.model.symbol.SourceType.USER_DEFINED);
    AddressSet b = new AddressSet(f.getBody()); b.add(s, e); f.setBody(b);
    println("MKFN " + f.getName() + " " + f.getBody() + " ret_in=" + (getFunctionContaining(e)==f));
  }
}
