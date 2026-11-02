import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
public class FixRets extends GhidraScript {
  public void run() throws Exception {
    for (String a : getScriptArgs()) {
      Address ad = toAddr(Long.parseLong(a,16));
      Instruction prev = getInstructionBefore(ad);
      Function f = prev==null?null:getFunctionContaining(prev.getAddress());
      if (f==null) { println("FIXRET " + a + " NO_OWNER prev=" + prev); continue; }
      AddressSet s = new AddressSet(f.getBody());
      s.add(ad, ad.add(3));
      f.setBody(s);
      println("FIXRET " + a + " -> " + f.getName() + "@" + f.getEntryPoint() + " now contains=" + (getFunctionContaining(ad)==f));
    }
  }
}
