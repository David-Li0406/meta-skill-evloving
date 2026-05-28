/**
 * Health Check Script - Antigravity Skill
 * Verifica o status da API e serviços do CarInsight
 */

const BASE_URL = process.env.API_URL || 'http://localhost:3000';

interface HealthResponse {
    status: string;
    timestamp: string;
    services?: {
        database?: string;
        llm?: string;
        embeddings?: string;
    };
}

async function checkHealth(): Promise<void> {
    console.log('🩺 Verificando status do CarInsight...\n');

    try {
        const response = await fetch(`${BASE_URL}/admin/health`);
        const data: HealthResponse = await response.json();

        if (response.ok) {
            console.log('✅ API Online');
            console.log(`   Status: ${data.status}`);
            console.log(`   Timestamp: ${data.timestamp}`);

            if (data.services) {
                console.log('\n📊 Serviços:');
                Object.entries(data.services).forEach(([service, status]) => {
                    const icon = status === 'ok' || status === 'healthy' ? '✅' : '❌';
                    console.log(`   ${icon} ${service}: ${status}`);
                });
            }
        } else {
            console.log('⚠️ API respondendo com problemas');
            console.log(`   Status HTTP: ${response.status}`);
        }
    } catch (error) {
        console.log('❌ API Offline ou inacessível');
        console.log(`   URL: ${BASE_URL}`);
        console.log(`   Erro: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
        console.log('\n💡 Dica: Verifique se o servidor está rodando com "npm run dev"');
    }
}

checkHealth();
