import { julesFetch, ListSourcesResponse } from './client.js';

async function main() {
  try {
    const listResponse = await julesFetch<ListSourcesResponse>('sources?pageSize=30');

    if (!listResponse.sources || listResponse.sources.length === 0) {
      console.log('No sources found.');
      return;
    }

    console.log('Jules Sources:');
    listResponse.sources.forEach(source => {
      console.log('--------------------------------------------------');
      console.log(`Name: ${source.name}`);
      console.log(`ID: ${source.id}`);
      if (source.githubRepo) {
        console.log(`Repo: ${source.githubRepo.owner}/${source.githubRepo.repo}`);
        console.log(`Default Branch: ${source.githubRepo.defaultBranch?.displayName}`);
      }
    });
    console.log('--------------------------------------------------');

    if (listResponse.nextPageToken) {
        console.log(`\n(Has more pages. Next Page Token: ${listResponse.nextPageToken})`);
    }

  } catch (error) {
    process.exit(1);
  }
}

main();
