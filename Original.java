public class Main {

    public static int doMyCalculation(int valueFirst, int valueSecond) {
        int resultOfCalcInFunction = valueFirst - valueSecond;
        return resultOfCalcInFunction;
    }

    public static void main(String[] args) {
        int resultOfMyCalculation;
        int firstValue = 20;
        int secondValue = 6;
        resultOfMyCalculation = doMyCalculation(firstValue, secondValue);
        System.out.println("Hello World! ********** " + resultOfMyCalculation + " **********");
    }
}
