import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../..');

// Load env vars
dotenv.config({ path: path.resolve(projectRoot, '.env.local') });
dotenv.config({ path: path.resolve(projectRoot, '.env') });

const supabaseUrl = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error('❌ Missing Supabase credentials in environment.');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkSchema() {
    console.log('🔍 Checking database schema and data consistency...');

    // Check for legacy column usage in photo_libraries
    try {
        const { data: libraries, error } = await supabase
            .from('photo_libraries')
            .select('id, name, slug, google_drive_folder_id, gdrive_folder_id');

        if (error) throw error;

        console.log(`\nChecking ${libraries.length} photo libraries...`);

        let issuesFound = 0;

        libraries.forEach(lib => {
            // Check: Modern column missing but legacy present
            if (!lib.google_drive_folder_id && lib.gdrive_folder_id) {
                console.warn(`⚠️  Library "${lib.name}" (${lib.slug}):`);
                console.warn(`    - google_drive_folder_id is NULL`);
                console.warn(`    - gdrive_folder_id is SET ('${lib.gdrive_folder_id}')`);
                console.warn(`    -> Application logic must check BOTH or data should be migrated.`);
                issuesFound++;
            }
        });

        if (issuesFound > 0) {
            console.log(`\n❌ Found ${issuesFound} libraries with potential column mismatch issues.`);
            console.log('   (These prompted the recent sync bug. Ensure your API handles fallback or migrate data.)');
        } else {
            console.log('\n✅ All libraries use modern `google_drive_folder_id` or correctly lack it.');
        }

    } catch (err) {
        console.error('❌ Database check failed:', err.message);
        if (err.message.includes('relation "photo_libraries" does not exist')) {
            console.error('   Table not found. Is your database set up?');
        }
    }

    // Add more checks here as needed
}

checkSchema();
