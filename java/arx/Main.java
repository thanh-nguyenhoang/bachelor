package arx;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import org.deidentifier.arx.*;
import org.deidentifier.arx.AttributeType.Hierarchy;
import org.deidentifier.arx.criteria.KAnonymity;
import org.deidentifier.arx.ARXConfiguration.AnonymizationAlgorithm;
import org.deidentifier.arx.metric.InformationLoss;
import org.deidentifier.arx.ARXResult;
import org.deidentifier.arx.Data;
import org.deidentifier.arx.DataHandle;
import org.deidentifier.arx.metric.Metric;
import org.deidentifier.arx.metric.v2.__MetricV2;

public class Main{

	protected static void print(DataHandle handle) {
		Iterator<String[]> itHandle = handle.iterator();
		print(itHandle);
	}

	protected static void print(Iterator<String[]> iterator) {
		while(iterator.hasNext()) {
			System.out.print("   ");
			System.out.println(Arrays.toString((Object[])iterator.next()));
		}

	}

	protected static void printArray(String[][] array) {
		System.out.print("{");

		for(int j = 0; j < array.length; ++j) {
			String[] next = array[j];
			System.out.print("{");

			for(int i = 0; i < next.length; ++i) {
				String string = next[i];
				System.out.print("\"" + string + "\"");
				if (i < next.length - 1) {
					System.out.print(",");
				}
			}

			System.out.print("}");
			if (j < array.length - 1) {
				System.out.print(",\n");
			}
		}

		System.out.println("}");
	}

	protected static void printHandle(DataHandle handle) {
		Iterator<String[]> itHandle = handle.iterator();
		printIterator(itHandle);
	}

	protected static void printIterator(Iterator<String[]> iterator) {
		while(iterator.hasNext()) {
			String[] next = (String[])iterator.next();
			System.out.print("[");

			for(int i = 0; i < next.length; ++i) {
				String string = next[i];
				System.out.print(string);
				if (i < next.length - 1) {
					System.out.print(", ");
				}
			}

			System.out.println("]");
		}

	}
	protected static void printResult(ARXResult result, Data data) {
		DecimalFormat df1 = new DecimalFormat("#####0.00");
		String var10000 = df1.format((double)result.getTime() / 1000.0D);
		String sTotal = var10000 + "s";
		System.out.println(" - Time needed: " + sTotal);
		ARXLattice.ARXNode optimum = result.getGlobalOptimum();
		List<String> qis = new ArrayList(data.getDefinition().getQuasiIdentifyingAttributes());
		if (optimum == null) {
			System.out.println(" - No solution found!");
		} else {
			StringBuffer[] identifiers = new StringBuffer[qis.size()];
			StringBuffer[] generalizations = new StringBuffer[qis.size()];
			int lengthI = 0;
			int lengthG = 0;

			int i;
			for(i = 0; i < qis.size(); ++i) {
				identifiers[i] = new StringBuffer();
				generalizations[i] = new StringBuffer();
				identifiers[i].append((String)qis.get(i));
				generalizations[i].append(optimum.getGeneralization((String)qis.get(i)));
				if (data.getDefinition().isHierarchyAvailable((String)qis.get(i))) {
					generalizations[i].append("/").append(data.getDefinition().getHierarchy((String)qis.get(i))[0].length - 1);
				}

				lengthI = Math.max(lengthI, identifiers[i].length());
				lengthG = Math.max(lengthG, generalizations[i].length());
			}

			for(i = 0; i < qis.size(); ++i) {
				while(identifiers[i].length() < lengthI) {
					identifiers[i].append(" ");
				}

				while(generalizations[i].length() < lengthG) {
					generalizations[i].insert(0, " ");
				}
			}

			PrintStream var11 = System.out;
			InformationLoss var10001 = result.getGlobalOptimum().getLowestScore();
			var11.println(" - Information loss: " + var10001 + " / " + result.getGlobalOptimum().getHighestScore());
			System.out.println(" - Optimal generalization");

			for(i = 0; i < qis.size(); ++i) {
				System.out.println("   * " + identifiers[i] + ": " + generalizations[i]);
			}

			System.out.println(" - Statistics");
			System.out.println(result.getOutput(result.getGlobalOptimum(), false).getStatistics().getEquivalenceClassStatistics());
		}
	}

    /**
     * Entry point.
     * 
     * @param args
     *            the arguments
     * @throws IOException 
     */
    public static void main(String[] args) throws IOException {
		// TODO:get path from Activities through command lind
		String filePath = args[0];
		// String filePath = "./results/step1/associationNaiv.csv";
    	List<List<String>> records = new ArrayList<>();
    	try (BufferedReader br = new BufferedReader(new FileReader(filePath))){
    		String line;
    		while ((line = br.readLine()) != null) {
				String[] values = line.split(",");
    			records.add(Arrays.asList(values));
			}
		}

		Data data = Data.create(filePath, StandardCharsets.UTF_8, ',');

		// Check if Hierarchy exists, otherwise set AttributeType to insensitive
		List<String> headers = records.get(0);
		String header = headers.get(0);
		data.getDefinition().setAttributeType(header, AttributeType.INSENSITIVE_ATTRIBUTE);
    	for (int i = 0; i < headers.size(); i++) {
			String head = headers.get(i);
			data.getDefinition().setAttributeType(head, AttributeType.QUASI_IDENTIFYING_ATTRIBUTE);
			data.getDefinition().setAttributeType(head, Hierarchy.create("./data/ActivityHierarchyFinal.csv", StandardCharsets.UTF_8, ','));
		}

		ARXAnonymizer anonymizer = new ARXAnonymizer();

		ARXConfiguration config = ARXConfiguration.create();
		config.addPrivacyModel(new KAnonymity(Integer.parseInt(args[1])));
		config.setSuppressionLimit(0.1d); // Recommended default: 1d
		for (int i = 0; i < headers.size(); i++) {
			String head = headers.get(i);
			config.setAttributeWeight(head, 0.5d);
		}

		// config.setQualityModel(Metric.createEntropyMetric());
		// config.setQualityModel(__MetricV2.createLossMetric());
		// config.setSuppressionAlwaysEnabled(false);
		config.setHeuristicSearchTimeLimit(1000000);
		config.setAlgorithm(AnonymizationAlgorithm.BEST_EFFORT_GENETIC);
		ARXResult result = anonymizer.anonymize(data, config);

		printResult(result, data);

		/*
		System.out.println(" - Transformed data:");
		Iterator<String[]> transformed = result.getOutput(false).iterator();
		while (transformed.hasNext()) {
			System.out.print(">>>");
			System.out.println(Arrays.toString(transformed.next()));
		}
		*/
		result.getOutput(false).save("./results/step2/generalizedData.csv", ';');
    }
}
