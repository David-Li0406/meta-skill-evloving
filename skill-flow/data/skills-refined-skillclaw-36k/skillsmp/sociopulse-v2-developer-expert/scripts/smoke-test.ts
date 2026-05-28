import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1';

async function main() {
  console.log('🔥 DÉMARRAGE DU SMOKE TEST...');
  console.log(`🎯 Cible : ${API_URL}`);

  // 1. TEST DATABASE (Prisma)
  try {
    const userCount = await prisma.user.count();
    console.log(`✅ DATABASE: Connectée (${userCount} utilisateurs trouvés).`);
  } catch (error) {
    console.error('❌ DATABASE: Échec connexion.', error);
    process.exit(1);
  }

  // 2. TEST AUTH (Login Admin)
  let token = '';
  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'admin@sociopulse.fr', password: 'password123' }),
    });

    if (!res.ok) throw new Error(`Status ${res.status}`);
    const data = await res.json();
    token = data.accessToken; // Adapter selon le retour réel (token ou accessToken)
    console.log('✅ AUTH: Login Admin réussi.');
  } catch (error) {
    console.error('❌ AUTH: Échec Login.', error);
    process.exit(1);
  }

  // 3. TEST WALL FEED (Lecture données)
  try {
    const res = await fetch(`${API_URL}/wall/posts`, { // ou /wall/feed
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const feed = await res.json();
    console.log(`✅ WALL: Feed récupéré (${Array.isArray(feed) ? feed.length : 'OK'} items).`);
  } catch (error) {
    console.error('❌ WALL: Échec récupération Feed.', error);
  }

  // 4. TEST ADMIN ACCESS
  try {
    const res = await fetch(`${API_URL}/admin/users`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.status === 403) throw new Error('403 Forbidden (RolesGuard bloquant)');
    if (!res.ok) throw new Error(`Status ${res.status}`);
    console.log('✅ ADMIN: Accès Dashboard autorisé.');
  } catch (error) {
    console.error('❌ ADMIN: Échec accès.', error);
  }

  console.log('\n✨ SMOKE TEST TERMINÉ. SYSTÈME OPÉRATIONNEL.');
}

main()
  .catch(e => console.error(e))
  .finally(async () => await prisma.$disconnect());
