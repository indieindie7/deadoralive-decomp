// DeleteTiny.java <list.txt>: remove functions whose entry (hex per line) is listed (junk seeded in data).
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import java.nio.file.*;

public class DeleteTiny extends GhidraScript {
	@Override
	public void run() throws Exception {
		int n = 0;
		for (String l : Files.readAllLines(Paths.get(getScriptArgs()[0]))) {
			l = l.trim();
			if (l.isEmpty()) continue;
			Function f = getFunctionAt(toAddr(Long.parseLong(l.startsWith("0x") ? l.substring(2) : l, 16)));
			if (f != null) { removeFunction(f); n++; }
		}
		println("deleted " + n);
	}
}
