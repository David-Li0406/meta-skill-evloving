# Synthetic Data Generation

## Patterns

### **Llm Synthetic Generation**
  #### **Description**
Generate synthetic data using LLMs
  #### **When**
Need diverse, contextual training examples
  #### **Implementation**
    import Anthropic from "@anthropic-ai/sdk";
    import { z } from "zod";
    import { zodToJsonSchema } from "zod-to-json-schema";
    
    const anthropic = new Anthropic();
    
    // Define the schema for your synthetic data
    const CustomerSupportTicket = z.object({
      id: z.string().describe("Unique ticket ID"),
      category: z.enum(["billing", "technical", "account", "shipping", "other"]),
      sentiment: z.enum(["positive", "neutral", "negative", "frustrated"]),
      query: z.string().describe("Customer's question or issue"),
      idealResponse: z.string().describe("Ideal support agent response"),
      difficulty: z.enum(["easy", "medium", "hard"]),
      metadata: z.object({
        requiresEscalation: z.boolean(),
        estimatedHandleTime: z.number().describe("Minutes to resolve"),
      }),
    });
    
    interface GenerationConfig {
      count: number;
      diversity: "low" | "medium" | "high";
      biasCheck?: boolean;
      temperature?: number;
    }
    
    async function generateSyntheticData<T extends z.ZodType>(
      schema: T,
      context: string,
      config: GenerationConfig
    ): Promise<z.infer<T>[]> {
      const { count, diversity, biasCheck = true, temperature = 0.8 } = config;
    
      const results: z.infer<T>[] = [];
      const batchSize = 5;
      const seenExamples: string[] = [];
    
      for (let i = 0; i < count; i += batchSize) {
        const batchCount = Math.min(batchSize, count - i);
    
        const response = await anthropic.messages.create({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4096,
          temperature: diversity === "high" ? 1.0 : diversity === "medium" ? 0.8 : 0.5,
          system: `You are a synthetic data generator. Generate realistic, diverse data samples.
    
          Rules:
          - Each example must be unique and realistic
          - Vary the complexity and edge cases
          - Include both typical and edge-case scenarios
          - Do NOT copy exact phrases from examples - create new variations
          ${biasCheck ? "- Ensure demographic diversity in examples" : ""}
          ${seenExamples.length > 0 ? `- Avoid similarity to these already generated: ${seenExamples.slice(-10).join(", ")}` : ""}`,
          messages: [
            {
              role: "user",
              content: `Generate ${batchCount} synthetic examples for: ${context}
    
              Output as a JSON array matching this schema:
              ${JSON.stringify(zodToJsonSchema(schema), null, 2)}
    
              Generate diverse examples with varied difficulty and scenarios.`,
            },
          ],
        });
    
        const content = response.content[0];
        if (content.type !== "text") continue;
    
        // Parse and validate
        const parsed = JSON.parse(extractJSON(content.text));
        const items = Array.isArray(parsed) ? parsed : [parsed];
    
        for (const item of items) {
          const validated = schema.safeParse(item);
          if (validated.success) {
            results.push(validated.data);
            // Track for diversity
            seenExamples.push(JSON.stringify(item).slice(0, 100));
          }
        }
      }
    
      return results;
    }
    
    function extractJSON(text: string): string {
      const match = text.match(/\[[\s\S]*\]|\{[\s\S]*\}/);
      return match ? match[0] : text;
    }
    
    // Usage
    const syntheticTickets = await generateSyntheticData(
      CustomerSupportTicket,
      "Customer support tickets for an e-commerce platform. Include billing issues, technical problems, and shipping complaints.",
      { count: 100, diversity: "high", biasCheck: true }
    );
    
### **Sdv Tabular Synthesis**
  #### **Description**
Generate synthetic tabular data with SDV
  #### **When**
Need statistically accurate tabular data
  #### **Implementation**
    // Note: SDV is Python-based, here's a Node.js wrapper approach
    import { spawn } from "child_process";
    import { writeFile, readFile } from "fs/promises";
    import { z } from "zod";
    
    interface SDVConfig {
      synthesizer: "gaussian_copula" | "ctgan" | "tvae";
      sampleSize: number;
      constraints?: Array<{
        type: "unique" | "positive" | "range" | "custom";
        column: string;
        params?: Record<string, unknown>;
      }>;
    }
    
    async function generateWithSDV<T>(
      sourceData: T[],
      config: SDVConfig
    ): Promise<T[]> {
      // Write source data to temp file
      const inputPath = `/tmp/sdv_input_${Date.now()}.json`;
      const outputPath = `/tmp/sdv_output_${Date.now()}.json`;
    
      await writeFile(inputPath, JSON.stringify(sourceData));
    
      // Python script for SDV
      const pythonScript = `
          import json
          import sys
          from sdv.single_table import GaussianCopulaSynthesizer, CTGANSynthesizer, TVAESynthesizer
          from sdv.metadata import SingleTableMetadata
          import pandas as pd
    
          # Load data
          with open('${inputPath}', 'r') as f:
              data = json.load(f)
    
          df = pd.DataFrame(data)
    
          # Detect metadata
          metadata = SingleTableMetadata()
      metadata.detect_from_dataframe(df)
    
      # Choose synthesizer
      synthesizer_map = {
          'gaussian_copula': GaussianCopulaSynthesizer,
          'ctgan': CTGANSynthesizer,
          'tvae': TVAESynthesizer,
      }
    
      Synthesizer = synthesizer_map['${config.synthesizer}']
      synthesizer = Synthesizer(metadata)
    
      # Fit and sample
      synthesizer.fit(df)
      synthetic = synthesizer.sample(${config.sampleSize})
    
      # Save output
      synthetic.to_json('${outputPath}', orient='records')
      `;
    
      // Run Python script
      await new Promise((resolve, reject) => {
        const proc = spawn("python3", ["-c", pythonScript]);
        proc.on("close", (code) => {
          if (code === 0) resolve(null);
          else reject(new Error(`SDV failed with code ${code}`));
        });
      });
    
      // Read results
      const output = await readFile(outputPath, "utf-8");
      return JSON.parse(output);
    }
    
    // Validate synthetic data quality
    interface QualityMetrics {
      columnShapes: number; // 0-1, higher is better
      columnPairTrends: number;
      overallScore: number;
    }
    
    async function validateSyntheticQuality(
      real: unknown[],
      synthetic: unknown[]
    ): Promise<QualityMetrics> {
      const pythonScript = `
        import json
        from sdv.evaluation.single_table import evaluate_quality
        import pandas as pd
    
        real_df = pd.DataFrame(${JSON.stringify(real)})
        synthetic_df = pd.DataFrame(${JSON.stringify(synthetic)})
    
        report = evaluate_quality(real_df, synthetic_df)
        print(json.dumps({
            'columnShapes': report.get_property('Column Shapes'),
            'columnPairTrends': report.get_property('Column Pair Trends'),
            'overallScore': report.get_score()
        }))
      `;
    
      // Execute and parse
      return new Promise((resolve, reject) => {
        const proc = spawn("python3", ["-c", pythonScript]);
        let output = "";
        proc.stdout.on("data", (data) => (output += data));
        proc.on("close", (code) => {
          if (code === 0) resolve(JSON.parse(output));
          else reject(new Error("Quality check failed"));
        });
      });
    }
    
### **Faker Test Data**
  #### **Description**
Generate test data with Faker
  #### **When**
Need simple mock data for testing
  #### **Implementation**
    import { faker } from "@faker-js/faker";
    
    // Seed for reproducibility
    faker.seed(12345);
    
    interface UserProfile {
      id: string;
      email: string;
      name: string;
      avatar: string;
      address: {
        street: string;
        city: string;
        country: string;
        zipCode: string;
      };
      company: string;
      createdAt: Date;
      subscription: "free" | "pro" | "enterprise";
    }
    
    function generateUser(overrides?: Partial<UserProfile>): UserProfile {
      return {
        id: faker.string.uuid(),
        email: faker.internet.email(),
        name: faker.person.fullName(),
        avatar: faker.image.avatar(),
        address: {
          street: faker.location.streetAddress(),
          city: faker.location.city(),
          country: faker.location.country(),
          zipCode: faker.location.zipCode(),
        },
        company: faker.company.name(),
        createdAt: faker.date.past({ years: 2 }),
        subscription: faker.helpers.arrayElement(["free", "pro", "enterprise"]),
        ...overrides,
      };
    }
    
    // Generate batch with realistic distribution
    function generateUsers(count: number): UserProfile[] {
      return Array.from({ length: count }, () => {
        // Realistic subscription distribution
        const subscriptionWeights = { free: 0.7, pro: 0.25, enterprise: 0.05 };
        const subscription = faker.helpers.weightedArrayElement(
          Object.entries(subscriptionWeights).map(([value, weight]) => ({ value, weight }))
        ) as UserProfile["subscription"];
    
        return generateUser({ subscription });
      });
    }
    
    // Generate related data (orders for users)
    interface Order {
      id: string;
      userId: string;
      total: number;
      status: "pending" | "shipped" | "delivered" | "cancelled";
      items: number;
      createdAt: Date;
    }
    
    function generateOrdersForUsers(users: UserProfile[], avgOrdersPerUser: number): Order[] {
      return users.flatMap((user) => {
        // Pro/enterprise users order more
        const multiplier =
          user.subscription === "enterprise" ? 3 : user.subscription === "pro" ? 2 : 1;
        const orderCount = faker.number.int({
          min: 0,
          max: avgOrdersPerUser * multiplier * 2,
        });
    
        return Array.from({ length: orderCount }, () => ({
          id: faker.string.uuid(),
          userId: user.id,
          total: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
          status: faker.helpers.arrayElement(["pending", "shipped", "delivered", "cancelled"]),
          items: faker.number.int({ min: 1, max: 10 }),
          createdAt: faker.date.between({ from: user.createdAt, to: new Date() }),
        }));
      });
    }
    
### **Llm Data Augmentation**
  #### **Description**
Augment existing data with LLM variations
  #### **When**
Need more training examples from limited data
  #### **Implementation**
    import OpenAI from "openai";
    
    const openai = new OpenAI();
    
    interface AugmentationConfig {
      techniques: Array<"paraphrase" | "formalize" | "simplify" | "translate" | "noise">;
      preserveIntent: boolean;
      targetCount: number;
    }
    
    async function augmentTextData(
      examples: string[],
      config: AugmentationConfig
    ): Promise<string[]> {
      const augmented: string[] = [...examples]; // Keep originals
    
      const techniquesPrompt = {
        paraphrase: "Rephrase this text while keeping the exact same meaning",
        formalize: "Rewrite in a more formal, professional tone",
        simplify: "Simplify to a 6th grade reading level",
        translate: "Translate to Spanish then back to English (back-translation)",
        noise: "Add realistic typos and casual language",
      };
    
      for (const example of examples) {
        for (const technique of config.techniques) {
          if (augmented.length >= config.targetCount) break;
    
          const response = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
              {
                role: "system",
                content: `${techniquesPrompt[technique]}.
                ${config.preserveIntent ? "CRITICAL: The core meaning and intent must be preserved exactly." : ""}
                Output only the transformed text, nothing else.`,
              },
              { role: "user", content: example },
            ],
            temperature: 0.7,
          });
    
          const augmentedText = response.choices[0].message.content?.trim();
          if (augmentedText && augmentedText !== example) {
            augmented.push(augmentedText);
          }
        }
      }
    
      return augmented.slice(0, config.targetCount);
    }
    
    // Augment labeled data (preserves labels)
    interface LabeledExample {
      text: string;
      label: string;
      metadata?: Record<string, unknown>;
    }
    
    async function augmentLabeledData(
      examples: LabeledExample[],
      config: AugmentationConfig
    ): Promise<LabeledExample[]> {
      const augmented: LabeledExample[] = [...examples];
    
      for (const example of examples) {
        const variations = await augmentTextData([example.text], {
          ...config,
          targetCount: Math.ceil(config.targetCount / examples.length),
        });
    
        for (const variation of variations) {
          if (variation !== example.text) {
            augmented.push({
              text: variation,
              label: example.label, // Preserve label
              metadata: {
                ...example.metadata,
                augmented: true,
                source: example.text.slice(0, 50),
              },
            });
          }
        }
      }
    
      return augmented;
    }
    
### **Quality Validation**
  #### **Description**
Validate synthetic data quality
  #### **When**
After generating synthetic data
  #### **Implementation**
    import { z } from "zod";
    
    interface QualityReport {
      fidelity: {
        distributionMatch: number; // 0-1
        correlationMatch: number;
        schemaCompliance: number;
      };
      diversity: {
        uniqueness: number; // % unique examples
        coverageScore: number; // How well it covers the space
        duplicateCount: number;
      };
      utility: {
        modelPerformanceReal: number;
        modelPerformanceSynthetic: number;
        performanceGap: number;
      };
      privacy: {
        nearestNeighborDistance: number;
        membershipInferenceRisk: number;
        attributeInferenceRisk: number;
      };
      overall: number;
      recommendations: string[];
    }
    
    async function validateSyntheticData<T>(
      realData: T[],
      syntheticData: T[],
      schema: z.ZodType<T>
    ): Promise<QualityReport> {
      const recommendations: string[] = [];
    
      // 1. Schema compliance
      let schemaCompliance = 0;
      for (const item of syntheticData) {
        if (schema.safeParse(item).success) schemaCompliance++;
      }
      schemaCompliance /= syntheticData.length;
    
      if (schemaCompliance < 0.95) {
        recommendations.push("Schema compliance below 95%. Validate generation prompts.");
      }
    
      // 2. Uniqueness
      const serialized = syntheticData.map((d) => JSON.stringify(d));
      const unique = new Set(serialized);
      const uniqueness = unique.size / syntheticData.length;
      const duplicateCount = syntheticData.length - unique.size;
    
      if (uniqueness < 0.9) {
        recommendations.push("High duplicate rate. Increase diversity in generation.");
      }
    
      // 3. Distribution comparison (simplified)
      const numericFields = getNumericFields(realData[0] as Record<string, unknown>);
      let distributionMatch = 0;
    
      for (const field of numericFields) {
        const realValues = realData.map((d) => (d as Record<string, number>)[field]);
        const synthValues = syntheticData.map((d) => (d as Record<string, number>)[field]);
    
        const realMean = mean(realValues);
        const synthMean = mean(synthValues);
        const realStd = std(realValues);
        const synthStd = std(synthValues);
    
        // Compare means and stds
        const meanDiff = Math.abs(realMean - synthMean) / (realMean || 1);
        const stdDiff = Math.abs(realStd - synthStd) / (realStd || 1);
    
        distributionMatch += 1 - (meanDiff + stdDiff) / 2;
      }
      distributionMatch /= numericFields.length || 1;
    
      if (distributionMatch < 0.8) {
        recommendations.push("Distribution mismatch detected. Review generation parameters.");
      }
    
      // 4. Privacy check (simplified - check for exact matches)
      const realSet = new Set(realData.map((d) => JSON.stringify(d)));
      let memorizedCount = 0;
      for (const item of syntheticData) {
        if (realSet.has(JSON.stringify(item))) memorizedCount++;
      }
    
      const memorizedRatio = memorizedCount / syntheticData.length;
      if (memorizedRatio > 0.01) {
        recommendations.push(
          `WARNING: ${(memorizedRatio * 100).toFixed(1)}% synthetic data matches real data exactly. Privacy risk.`
        );
      }
    
      return {
        fidelity: {
          distributionMatch,
          correlationMatch: 0.85, // Would need proper calculation
          schemaCompliance,
        },
        diversity: {
          uniqueness,
          coverageScore: Math.min(1, syntheticData.length / realData.length),
          duplicateCount,
        },
        utility: {
          modelPerformanceReal: 0, // Requires training
          modelPerformanceSynthetic: 0,
          performanceGap: 0,
        },
        privacy: {
          nearestNeighborDistance: 0,
          membershipInferenceRisk: memorizedRatio,
          attributeInferenceRisk: 0,
        },
        overall: (schemaCompliance + uniqueness + distributionMatch) / 3,
        recommendations,
      };
    }
    
    function getNumericFields(obj: Record<string, unknown>): string[] {
      return Object.entries(obj)
        .filter(([_, v]) => typeof v === "number")
        .map(([k]) => k);
    }
    
    function mean(arr: number[]): number {
      return arr.reduce((a, b) => a + b, 0) / arr.length;
    }
    
    function std(arr: number[]): number {
      const m = mean(arr);
      return Math.sqrt(arr.reduce((sum, x) => sum + (x - m) ** 2, 0) / arr.length);
    }
    
### **Instruction Tuning Data**
  #### **Description**
Generate instruction-tuning datasets
  #### **When**
Fine-tuning LLMs for specific tasks
  #### **Implementation**
    import Anthropic from "@anthropic-ai/sdk";
    import { z } from "zod";
    
    const anthropic = new Anthropic();
    
    const InstructionExample = z.object({
      instruction: z.string().describe("Clear task instruction"),
      input: z.string().optional().describe("Optional input context"),
      output: z.string().describe("Expected model response"),
      category: z.string().describe("Task category"),
      difficulty: z.enum(["easy", "medium", "hard"]),
    });
    
    type InstructionExample = z.infer<typeof InstructionExample>;
    
    interface InstructionDatasetConfig {
      taskDescription: string;
      categories: string[];
      examplesPerCategory: number;
      includeEdgeCases: boolean;
      format: "alpaca" | "sharegpt" | "openai";
    }
    
    async function generateInstructionDataset(
      config: InstructionDatasetConfig
    ): Promise<InstructionExample[]> {
      const allExamples: InstructionExample[] = [];
    
      for (const category of config.categories) {
        const response = await anthropic.messages.create({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4096,
          temperature: 0.9,
          messages: [
            {
              role: "user",
              content: `Generate ${config.examplesPerCategory} instruction-tuning examples for:
    
              Task: ${config.taskDescription}
              Category: ${category}
    
              Requirements:
              - Each example needs: instruction, input (optional), output
              - Vary difficulty: easy, medium, hard
              - Instructions should be clear and specific
              - Outputs should be high-quality examples of ideal responses
              ${config.includeEdgeCases ? "- Include edge cases and tricky scenarios" : ""}
    
              Output as JSON array with keys: instruction, input, output, category, difficulty`,
            },
          ],
        });
    
        const content = response.content[0];
        if (content.type === "text") {
          const examples = JSON.parse(extractJSON(content.text));
          for (const ex of examples) {
            const validated = InstructionExample.safeParse({ ...ex, category });
            if (validated.success) {
              allExamples.push(validated.data);
            }
          }
        }
      }
    
      return formatDataset(allExamples, config.format);
    }
    
    function formatDataset(
      examples: InstructionExample[],
      format: "alpaca" | "sharegpt" | "openai"
    ): InstructionExample[] {
      // Alpaca format is our base format
      if (format === "alpaca") return examples;
    
      // Convert to other formats as needed
      // ShareGPT format: { conversations: [{ from: "human", value: "" }, { from: "gpt", value: "" }] }
      // OpenAI format: { messages: [{ role: "system", content: "" }, ...] }
    
      return examples;
    }
    
    function extractJSON(text: string): string {
      const match = text.match(/\[[\s\S]*\]|\{[\s\S]*\}/);
      return match ? match[0] : text;
    }
    

## Anti-Patterns


---
  #### **Pattern**
Generate data without validation
  #### **Problem**
Synthetic data may not match real distribution
  #### **Solution**
Always validate with quality metrics before use

---
  #### **Pattern**
Using real data as few-shot examples
  #### **Problem**
Risk of memorization and privacy leakage
  #### **Solution**
Use separate seed examples that aren't from production

---
  #### **Pattern**
Single technique for all data
  #### **Problem**
Different data types need different approaches
  #### **Solution**
Use SDV for tabular, LLM for text, domain-specific for specialized data

---
  #### **Pattern**
No bias checking
  #### **Problem**
Synthetic data can amplify existing biases
  #### **Solution**
Audit for demographic representation and harmful patterns

---
  #### **Pattern**
Assuming privacy by default
  #### **Problem**
Synthetic data can leak information about real data
  #### **Solution**
Run privacy metrics and add differential privacy if needed