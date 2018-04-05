import com.scitools.understand.*;


public class Main {

    public static void main(String[] args) {
        try {
            //Open the Understand Database
            System.out.println("Hello World!");
            Database dbOriginal = Understand.open("C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/original.udb");
            Database dbNew = Understand.open("C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/new.udb");

            // Get a list of all functions and methods
//            Entity[] funcs = db.ents("variables");
//            Entity[] funcs2 = db.ents("variables");

            // Get a list of all interfaces and methods
            Entity[] entsOriginal = dbOriginal.ents("variable");
            Entity[] entsNew = dbNew.ents("variable");

            //Loop through the entity method and load the graph
            int entsLength = entsOriginal.length < entsNew.length? entsOriginal.length:entsNew.length;
            for(int i = 0; i < entsLength; i++) {
                System.out.println(entsOriginal[i].name() + ":" + entsOriginal[i].value());
                Reference[] paramRefsOriginal = entsOriginal[i].refs("CalledBy", "variable, parameter", true);
                Reference[] paramRefsNew = entsOriginal[i].refs("CalledBy", "variable, parameter", true);

                int refsLength = paramRefsOriginal.length < paramRefsNew.length? paramRefsOriginal.length:paramRefsNew.length;
                for(int j = 0; j < refsLength; j++) {

                    System.out.println(paramRefsOriginal[j].ent().name() + " = " + paramRefsNew[j].ent().name());
                    if(paramRefsOriginal[j].ent().name().equals(paramRefsNew[j].ent().name()) == false) {
                        System.out.println("******* Found a change *********");
                    }
                }

            }
//            for(Entity e : entsOriginal)
//            {
//                //Find out which variables and parameters are called by each method
//                Reference [] parameterRefs = e.refs("CalledBy","variable,parameter",true);
//
//                //Loop through each reference and input it into the graph
//                for( Reference pRef : parameterRefs){
//
//                    System.out.println("Entity: " + e.name());
//                    System.out.println("Kind: " + e.kind());
//                    System.out.println("Entity Reference Name: " + pRef.ent().name());
//                    System.out.println("Entity Reference Kind: " + pRef.ent().kind());
//                    System.out.println("Entity Reference Line: " + pRef.line());
//                    System.out.println("Entity Reference Scope: " + pRef.scope().name());
//                    System.out.println("Entity Reference File: " + pRef.file().name());
//                    System.out.println();
//                    //Remove local variables
//                    if(pRef.ent().name().contains("doMyCalculation")) {
//                        //Create an edge from entity to reference
//                        System.out.println("*****");
//                        //e.name(),pRef.ent().name();
//                    }
//                }
//                //For each method, see what other methods it calls
//                Reference [] parameterRef = e.refs("Call",null,true);
//                //Loop though it and load  it in your graph
//                for( Reference pRef : parameterRef){
//                }
//            }


//            for (Entity e : funcs) {
//                System.out.println(e.name());
//                System.out.print(e.name() + "(");
//
//                //Find all the parameters for the given method/function and build them into a string
//                StringBuilder paramList = new StringBuilder();
//                Reference[] paramterRefs = e.refs("define", "parameter", true);
//                for (Reference pRef : paramterRefs) {
//                    Entity pEnt = pRef.ent();
//                    paramList.append(pEnt.type() + " " + pEnt.name());
//                    paramList.append(",");
//                }
//
//                //Remove trailing comma from parameter list
//                if (paramList.length() > 0) {
//                    paramList.setLength(paramList.length() - 1);
//                }
//                System.out.print(paramList + ")\n");
//            }
        } catch (UnderstandException e) {
            System.out.println("Failed opening Database:" + e.getMessage());
            System.exit(0);
        }
    }
}



