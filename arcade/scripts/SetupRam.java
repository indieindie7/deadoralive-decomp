// SetupRam.java: RAM block 0x500000..0x5fffff + Fighter struct (0x58) applied at P1/P2
import ghidra.app.script.GhidraScript;
import ghidra.program.model.data.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
public class SetupRam extends GhidraScript {
	void f(StructureDataType s,int off,DataType t,String n,String c){ s.replaceAtOffset(off,t,t.getLength(),n,c); }
	@Override public void run() throws Exception {
		Memory m=currentProgram.getMemory();
		Address a=toAddr(0x500000L);
		if(m.getBlock(a)==null){
			MemoryBlock b=m.createUninitializedBlock("WORKRAM",a,0x100000,false);
			b.setRead(true);b.setWrite(true);b.setExecute(false);
			println("created WORKRAM");
		}
		DataTypeManager dm=currentProgram.getDataTypeManager();
		StructureDataType s=new StructureDataType("Fighter",0x58);
		DataType u8=ByteDataType.dataType,u16=UnsignedShortDataType.dataType,u32=UnsignedIntegerDataType.dataType,fl=FloatDataType.dataType;
		String[][] b={{"0","mancom"},{"1","chrnum"},{"2","chrcol"},{"2a","moveid"},{"2b","actcodeflg"},{"30","updownhead"},{"32","attackpoint"},{"33","attacksta"},{"34","animeflip"},{"35","animeflg"},{"37","hitattack"},{"38","hitbody"},{"39","hitstage"},{"3e","beatsta"},{"3f","skysta"},{"40","downhit"},{"41","actcancel"},{"42","graspsta"},{"43","dwnasta"},{"44","mountsta"},{"46","atkheight"},{"47","ringhit"},{"4a","drctajstflg"},{"4b","damagenum"},{"4d","hitgrasp"},{"55","ac_use"}};
		for(String[] r:b) f(s,Integer.parseInt(r[0],16),u8,r[1],"proof: debug str / xref");
		f(s,0x4,fl,"pos_x","debug Xpos");f(s,0x8,fl,"pos_y","debug Ypos; landing check <=1.2 / fall KO <=0");f(s,0xc,fl,"pos_z","debug Zpos");
		f(s,0x14,u32,"drct","16.16 angle");f(s,0x18,u32,"atkdrct","16.16 angle");f(s,0x1c,u32,"bodydrct","16.16 angle");
		f(s,0x28,u16,"anime","debug anime");
		dm.addDataType(s,DataTypeConflictHandler.REPLACE_HANDLER);
		Listing l=currentProgram.getListing();
		for(int i=0;i<2;i++){
			Address p=toAddr(0x54fc00L+i*0x58);
			l.clearCodeUnits(p,p.add(0x57),false);
			l.createData(p,s);
			currentProgram.getSymbolTable().createLabel(p,"g_fighter"+(i+1),SourceType.USER_DEFINED);
		}
	}
}
