import com.scitools.understand.*;


public class Main {

    public static void main(String[] args) {
        try {
            //Open the Understand Database
            Database db = Understand.open("C:\\Users\\Viren\\Google Drive\\1. UIC\\540 - Advanced Software Engineering Topics\\test.udb");

            // Get a list of all functions and methods
            Entity[] funcs = db.ents("class, function");
            System.out.println("Hello World!");
            for (Entity e : funcs) {
                System.out.print(e.name() + "(");

                //Find all the parameters for the given method/function and build them into a string
                StringBuilder paramList = new StringBuilder();
                Reference[] paramterRefs = e.refs("define", "parameter", true);
                for (Reference pRef : paramterRefs) {
                    Entity pEnt = pRef.ent();
                    paramList.append(pEnt.type() + " " + pEnt.name());
                    paramList.append(",");
                }

                //Remove trailing comma from parameter list
                if (paramList.length() > 0) {
                    paramList.setLength(paramList.length() - 1);
                }
                System.out.print(paramList + ")\n");
            }
        } catch (UnderstandException e) {
            System.out.println("Failed opening Database:" + e.getMessage());
            System.exit(0);
        }
    }
}
