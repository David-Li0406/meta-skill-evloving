const fs = require('fs');
const path = require('path');

const SCHEMA_PATH = 'prisma/schema.prisma';

function auditSchema() {
    console.log('🔍 Starting Prisma Schema Audit...\n');

    if (!fs.existsSync(SCHEMA_PATH)) {
        console.error(`❌ Schema not found at ${SCHEMA_PATH}`);
        return;
    }

    const content = fs.readFileSync(SCHEMA_PATH, 'utf8');
    const lines = content.split('\n');

    let currentModel = null;
    let modelFields = [];
    let issues = [];

    // 1. Parse Models
    lines.forEach((line, index) => {
        const trimmed = line.trim();
        if (trimmed.startsWith('model ')) {
            currentModel = trimmed.split(' ')[1];
            modelFields = [];
        } else if (trimmed.startsWith('}') && currentModel) {
            // End of model, analyze it
            analyzeModel(currentModel, modelFields, issues);
            currentModel = null;
        } else if (currentModel && trimmed && !trimmed.startsWith('//') && !trimmed.startsWith('@@')) {
            // Parse field
            const parts = trimmed.split(/\s+/);
            if (parts.length >= 2) {
                // [name, type, attributes...]
                modelFields.push({
                    name: parts[0],
                    type: parts[1],
                    raw: line,
                    isRelation: trimmed.includes('@relation')
                });
            }
        } else if (currentModel && trimmed.startsWith('@@index')) {
            modelFields.push({ isIndex: true, raw: line });
        }
    });

    // 2. Report
    if (issues.length > 0) {
        console.log(`⚠️  Found ${issues.length} potential schema optimizations:`);
        issues.forEach(issue => console.log(`   ${issue}`));
    } else {
        console.log(`✅  Schema looks healthy!`);
    }
}

function analyzeModel(modelName, fields, issues) {
    // Find relations and their scalar fields
    fields.forEach(field => {
        if (field.isRelation) {
            // Extract "fields: [userId]"
            const match = field.raw.match(/fields:\s*\[([^\]]+)\]/);
            if (match) {
                const scalarFieldName = match[1];

                // Check if this scalar field is indexed
                // It is indexed if:
                // 1. It has @id or @unique or @index (inline) -- simplified check
                // 2. There is a @@index([field]) block

                const scalarField = fields.find(f => f.name === scalarFieldName);
                const hasInlineIndex = scalarField && (scalarField.raw.includes('@unique') || scalarField.raw.includes('@id'));

                // Check block indexes
                const hasBlockIndex = fields.some(f => f.isIndex && f.raw.includes(`[${scalarFieldName}]`));

                if (!hasInlineIndex && !hasBlockIndex) {
                    issues.push(`❌ [Missing Index] Model "${modelName}": Relation field "${scalarFieldName}" is not indexed. Prisma doesn't do this automatically.`);
                }
            }
        }
    });
}

auditSchema();
