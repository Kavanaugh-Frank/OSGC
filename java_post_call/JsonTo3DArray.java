package java_post_call;

public class JsonTo3DArray {
    public static void main(String[] args) {
        // just to get it right, to be combined with the post command response
        String jsonResponse = "{\n" +
                "  \"data\": \"[[[690780.6125821351,-4915159.4555769395,3992427.3177376995],[692926.1395656003,-4914864.3154589236,3992432.8277480812],[695071.6317871826,-4914568.8842073353,3992438.8656074707],[697217.7671491591,-4914277.9368175529,3992449.3368070018],[699361.0044282518,-4913966.5434231292,3992443.8508897116]],[[691031.2500985351,-4916942.8341724258,3990314.275810366],[693175.6942358034,-4916634.3848404977,3990308.9959324813],[695321.0320053796,-4916332.2917411942,3990309.6740336828],[697458.0467453225,-4915971.5263583371,3990263.1722077453],[699606.064816358,-4915688.4274581959,3990280.8996680793]],[[691272.5496446992,-4918659.7696572272,3988146.9330900251],[693415.7730038126,-4918337.2424791604,3988130.2517758543],[695568.0979345664,-4918079.1944666114,3988166.9726545354],[697705.4849216273,-4917715.5725198584,3988118.2682596436],[699857.0848207555,-4917452.185939908,3988152.1630216674]],[[691513.2815059657,-4920372.6658540964,3985976.3272542418],[693661.5209316316,-4920080.3109709807,3985984.3553305124],[695806.7484928981,-4919766.5955264987,3985975.7255559745],[697953.6822802211,-4919464.969710784,3985977.7203418566],[700094.6709707252,-4919121.5532405432,3985946.3883817401]],[[691757.0996872074,-4922107.5223586699,3983823.6509299451],[693905.6386680851,-4921811.8166584671,3983829.0281606666],[696054.9397363389,-4921521.4548914414,3983839.5245992034],[698193.7446566513,-4921157.0281974375,3983790.424616545],[700340.3083975828,-4920847.4917612048,3983786.819338588]]]\",\n" +
                "  \"shape\": [5, 5]\n" +
                "}";

        // extract the data part
        String dataString = jsonResponse.substring(jsonResponse.indexOf("\"data\": \"") + 9, jsonResponse.indexOf("\"", jsonResponse.indexOf("\"data\": \"") + 9));

        // prepare the string for splitting
        dataString = dataString.replaceAll("\\\\", ""); // remove escape characters
        String[] rowStrings = dataString.split("\\],\\["); // split by rows

        // remove the outer brackets for the first and last row
        for (int i = 0; i < rowStrings.length; i++) {
            rowStrings[i] = rowStrings[i].replaceAll("[\\[\\]]", ""); // remove square brackets
        }

        // create a 3d array
        double[][][] elevation = new double[rowStrings.length][][];

        for (int i = 0; i < rowStrings.length; i++) {
            // split by the inner array
            String[] points = rowStrings[i].split("\\],\\[");
            elevation[i] = new double[points.length][3]; // each point has 3 values (x, y, z)

            for (int j = 0; j < points.length; j++) {
            // remove any extra brackets and split by comma
            String[] values = points[j].replaceAll("[\\[\\]]", "").split(",");
            for (int k = 0; i < values.length; k++) {
                elevation[i][j][k] = Double.parseDouble(values[k].trim());
            }
            }
        }

        // output the results
        System.out.println(elevation.length);
        System.out.println("elevation array: ");
        for (double[][] row : elevation) {
            for (double[] point : row) {
            System.out.print(java.util.Arrays.toString(point) + " ");
            }
            System.out.println();
        }
    }
}
